"""
构建脚本：将 SeqDiff Visualizer 打包成单个 .exe
需要先安装: pip install pyinstaller flask
"""
import os
import subprocess
import sys

def build():
    print("=" * 50)
    print("  SeqDiff Visualizer 打包工具")
    print("=" * 50)
    print()
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # 检查 Flask
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError:
        print("正在安装 Flask...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask'], check=True)
    
    print()
    print("开始打包...")
    print()
    
    # 构建命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'SeqDiff',
        '--add-data', 'index.html;.',
        '--add-data', 'examples;examples',
        '--hidden-import', 'flask',
        '--console',  # 保留控制台窗口显示日志
        'app.py'
    ]
    
    # 如果 MAFFT 存在，也打包进去
    if os.path.exists('mafft-win'):
        cmd.insert(-1, '--add-data')
        cmd.insert(-1, 'mafft-win;mafft-win')
        print("✓ MAFFT 已包含在打包中")
    
    print("执行命令:")
    print(" ".join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print("=" * 50)
        print("✓ 打包成功！")
        print(f"  输出文件: dist/SeqDiff.exe")
        print(f"  大小: {os.path.getsize('dist/SeqDiff.exe') / 1024 / 1024:.1f} MB")
        print("=" * 50)
    else:
        print()
        print("✗ 打包失败，请检查错误信息")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
