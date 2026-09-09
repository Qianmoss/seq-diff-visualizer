"""
SeqDiff Visualizer - Flask Backend
调用本地 MAFFT 进行序列比对，返回结果给前端
"""
import os
import sys
import subprocess
import tempfile
import webbrowser
import threading
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

# MAFFT 可执行文件路径（兼容 PyInstaller 打包）
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAFFT_DIR = os.path.join(BASE_DIR, 'mafft-win')
MAFFT_BAT = os.path.join(MAFFT_DIR, 'mafft.bat')

def find_mafft():
    """查找 MAFFT 可执行文件"""
    if os.path.exists(MAFFT_BAT):
        return MAFFT_BAT
    # 尝试其他路径
    for name in ['mafft.bat', 'mafft.exe', 'mafft-signed.ps1']:
        for root, dirs, files in os.walk(MAFFT_DIR):
            for f in files:
                if f.lower() == name.lower():
                    return os.path.join(root, f)
    return None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/api/mafft-align', methods=['POST'])
def mafft_align():
    """调用 MAFFT 进行双序列比对"""
    data = request.json
    seq1 = data.get('seq1', '').strip()
    seq2 = data.get('seq2', '').strip()
    seq1_name = data.get('name1', 'Seq1')
    seq2_name = data.get('name2', 'Seq2')
    
    if not seq1 or not seq2:
        return jsonify({'error': '请提供两条序列'}), 400
    
    # Validate DNA characters
    import re
    valid_bases = re.compile(r'^[ATCGUNRYSWKMBDHV-]+$', re.IGNORECASE)
    if not valid_bases.match(seq1.replace(' ', '').replace('\n', '')):
        return jsonify({'error': '序列1包含非法字符'}), 400
    if not valid_bases.match(seq2.replace(' ', '').replace('\n', '')):
        return jsonify({'error': '序列2包含非法字符'}), 400
    
    mafft_path = find_mafft()
    if not mafft_path:
        return jsonify({'error': '未找到 MAFFT，请确认 mafft-win 文件夹中有 mafft.exe'}), 500
    
    # 创建临时 FASTA 文件 — 使用固定内部 ID，避免同名导致解析失败
    fasta_content = ">SeqDiff_1\n%s\n>SeqDiff_2\n%s\n" % (seq1, seq2)
    
    input_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False, encoding='utf-8') as f:
            f.write(fasta_content)
            input_file = f.name
        
        # 调用 MAFFT
        mafft_dir = os.path.dirname(mafft_path)
        # Use list form to handle paths with spaces properly
        cmd = ['cmd.exe', '/C', 'mafft.bat', '--auto', input_file]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            encoding='utf-8',
            errors='replace',
            shell=False,
            cwd=mafft_dir
        )
        
        if result.returncode != 0:
            return jsonify({'error': 'MAFFT 执行失败: ' + result.stderr[:500]}), 500
        
        # 解析输出 — 按固定内部 ID 提取
        output = result.stdout
        sequences = {}
        current_name = None
        current_seq = ""
        
        for line in output.strip().split('\n'):
            line = line.strip()
            if line.startswith('>'):
                if current_name:
                    sequences[current_name] = current_seq
                current_name = line[1:].strip()
                current_seq = ""
            elif line:
                current_seq += line
        if current_name:
            sequences[current_name] = current_seq
        
        aligned1 = sequences.get('SeqDiff_1', '')
        aligned2 = sequences.get('SeqDiff_2', '')
        
        if not aligned1 or not aligned2:
            return jsonify({'error': 'MAFFT 输出格式错误'}), 500
        
        return jsonify({
            'aligned1': aligned1,
            'aligned2': aligned2,
            'name1': seq1_name,
            'name2': seq2_name,
            'method': 'MAFFT --auto'
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'MAFFT 执行超时（120秒）'}), 500
    except Exception as e:
        return jsonify({'error': '执行出错: ' + str(e)}), 500
    finally:
        # 清理临时文件
        if input_file:
            try:
                os.unlink(input_file)
            except:
                pass

@app.route('/api/check-mafft')
def check_mafft():
    """检查 MAFFT 是否可用"""
    mafft_path = find_mafft()
    if mafft_path:
        return jsonify({'status': 'ok', 'path': mafft_path})
    else:
        return jsonify({'status': 'not_found', 'path': MAFFT_DIR})

def open_browser(port):
    """延迟打开浏览器"""
    import time
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{port}')

if __name__ == '__main__':
    port = 5000
    
    # 检查 MAFFT
    mafft_path = find_mafft()
    if mafft_path:
        print(f"[OK] MAFFT found: {mafft_path}")
    else:
        print(f"[WARN] MAFFT not found in: {MAFFT_DIR}")
    
    print(f"\nSeqDiff Visualizer starting...")
    print(f"Browser will open: http://localhost:{port}")
    print(f"Press Ctrl+C to stop\n")
    
    # 自动打开浏览器
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    app.run(host='127.0.0.1', port=port, debug=False)
