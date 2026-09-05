# SeqDiff Visualizer

🧬 基因序列差异位点可视化工具

一个基于 Flask + MAFFT 的本地序列比对工具，支持多种比对模式、碱基着色、裁剪和中英双语。

## 功能特性

- **三种比对模式**
  - 已比对：直接比较已比对好的序列
  - NW 自动比对：Needleman-Wunsch 算法自动比对
  - MAFFT 比对：调用本地 MAFFT 进行专业比对

- **可视化**
  - 碱基着色（A=绿 T=红 C=蓝 G=金）
  - 匹配/错配/空位背景高亮
  - 折行/单行显示切换
  - 悬停显示位点信息

- **数据统计**
  - 比对长度、差异数、差异率
  - 详细数据（匹配/错配/空位）
  - 含 gap / 不含 gap 两种统计

- **实用工具**
  - 裁剪碱基（可连续裁剪前后）
  - 差异位点列表（支持复制/导出 CSV）
  - 历史记录（最多保存 5 条）
  - 文件上传（支持 FASTA/TXT）

- **多语言**
  - 中文 / English 切换

## 快速开始

### 方式一：直接运行（推荐）

1. 下载并安装 [Python 3.12](https://www.python.org/downloads/)
2. 安装 Flask：
   ```bash
   pip install flask
   ```
3. 下载 [MAFFT Windows 版](https://mafft.cbrc.jp/alignment/software/mafft-7.526-win64-signed.zip)，解压到项目根目录的 `mafft-win` 文件夹
4. 运行：
   ```bash
   python app.py
   ```
5. 浏览器自动打开 http://localhost:5000

### 方式二：打包版（Windows）

下载 `dist/SeqDiff` 文件夹，双击 `SeqDiff.exe` 即可运行，无需安装 Python。

## 使用说明

1. **添加序列**：在文本框粘贴两条序列（支持 FASTA 格式），或点击上传文件
2. **选择模式**：已比对 / NW自动比对 / MAFFT比对
3. **开始计算**：点击「开始」查看差异位点、统计与可视化

## 项目结构

```
seq-diff-visualizer/
├── app.py              # Flask 后端
├── index.html          # 前端界面
├── 启动工具.bat         # Windows 启动脚本
├── 打包.bat             # PyInstaller 打包脚本
├── build.spec          # PyInstaller 配置
├── examples/           # 示例文件
│   └── sample_rDNA.fasta
├── mafft-win/          # MAFFT（需自行下载）
├── dist/               # 打包输出
├── LICENSE             # MIT 许可证
└── README.md           # 本文件
```

## 技术栈

- **后端**：Python 3.12 + Flask
- **前端**：原生 HTML/CSS/JavaScript（无框架依赖）
- **比对引擎**：MAFFT（本地调用）
- **打包**：PyInstaller

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

- [MAFFT](https://mafft.cbrc.jp/alignment/software/) - 序列比对算法
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
