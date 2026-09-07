# SeqDiff Visualizer

**v1.1.0 — Stability & Accuracy Update**

一个面向科研人员的 DNA 双序列比对与差异分析工具。输入两条序列，自动完成比对、统计 identity/mismatch/gap、定位差异位点，并提供 alignment position 与原始 sequence position 的坐标映射，支持结果导出。

## Workflow

```
Input FASTA / TXT
       ↓
  Needleman-Wunsch / MAFFT
       ↓
    Alignment
       ↓
  Difference Statistics
       ↓
  Difference-site Detection
       ↓
  Coordinate Mapping (Alignment ↔ Sequence Position)
       ↓
  Visualization / CSV Export
```

## Screenshots

| Input | Results |
| :---: | :---: |
| ![Input](./docs/screenshots/1-input.png) | ![Results](./docs/screenshots/2-result.png) |

## Features

**比对与统计**
- Pre-aligned 模式：直接比较已比对好的序列
- Needleman-Wunsch 自动比对（内置）
- MAFFT 自动比对（本地调用）
- GAP 处理策略：支持 gap-open / gap-extension 参数
- 自动统计：Identity / Mismatch rate / Gap rate / Variable sites

**差异分析**
- 差异位点检测：Mismatch / Gap 分类
- 坐标映射：Alignment Position ↔ Sequence 1 Position / Sequence 2 Position
- 差异表：完整展示每个差异位点的坐标和类型

**可视化**
- 碱基着色（A/T/C/G 四色）
- 折行 / 单行显示切换
- 悬停显示位点信息
- 长序列保护（>5000bp 自动简化视图）

**实用工具**
- 序列裁剪（可连续裁剪前后，自动更新统计）
- CSV 导出（含完整坐标信息）
- 差异结果复制
- 历史记录（最多 5 条）
- FASTA / TXT 文件上传

**界面**
- 中文 / English 双语切换
- Windows 绿色免安装版本

## Quick Start

### Windows 用户（推荐）

下载绿色免安装包，**已内置 MAFFT**，解压后即可使用，无需安装 Python、Flask 或额外配置环境变量。

1. 从 [Releases](https://github.com/Qianmoss/seq-diff-visualizer/releases) 下载 `SeqDiff.zip`
2. 解压到任意目录
3. 双击 `SeqDiff.exe`
4. 浏览器自动打开 http://localhost:5000

### Mac / Linux 用户

需要自行准备 Python 环境，并安装 MAFFT。

1. 安装 [Python 3.12](https://www.python.org/downloads/)
2. 安装 Flask：`pip install flask`
3. 下载 [MAFFT](https://mafft.cbrc.jp/alignment/software/)，解压到项目根目录的 `mafft-win` 文件夹
4. 运行：`python app.py`

## Usage Example

以 `examples/sample_rDNA.fasta` 中的两条 rDNA 序列为例：

**1. 输入序列**
- 方式 A：在文本框粘贴两条 FASTA 序列
- 方式 B：点击上传 `.fasta` 文件

**2. 选择比对模式**
- 已比对（Pre-aligned）：如果序列已经比对过
- NW 自动比对：使用 Needleman-Wunsch 算法
- MAFFT 比对：使用 MAFFT 专业比对

**3. 查看结果**
- 统计面板：Alignment length / Identity / Mismatch / Gap
- 差异表：每个差异位点的 Alignment Position 和 Sequence Position
- 可视化：碱基着色，一眼看出匹配/错配/空位

**4. 导出结果**
- 点击「导出 CSV」获得完整差异数据
- 包含：Alignment Position / Seq1 Position / Seq1 Base / Seq2 Position / Seq2 Base / Type

## Performance

- **≤ 3000 bp：** 完整逐位可视化，性能良好
- **3000–5000 bp：** 正常分析，可能提示渲染较慢
- **> 5000 bp：** 自动切换简化视图，避免浏览器卡顿

超长序列仍可进行比对和统计分析，仅可视化方式简化。

## Project Structure

```
seq-diff-visualizer/
├── app.py              # Flask 后端与程序入口
├── index.html          # 前端界面与交互逻辑
├── README.md
├── LICENSE
├── start.bat           # Windows 启动脚本
├── build.bat           # Windows 构建入口
├── build.py            # 打包辅助脚本
├── build.spec          # PyInstaller 配置
├── examples/
│   └── sample_rDNA.fasta
├── docs/
│   └── screenshots/
├── mafft-win/          # MAFFT（Release 已内置，源码需自行下载）
└── dist/               # PyInstaller 打包输出（构建产物）
```

## Tech Stack

- **后端**：Python 3.12 + Flask
- **前端**：原生 HTML / CSS / JavaScript（无框架依赖）
- **比对引擎**：MAFFT（本地调用）/ Needleman-Wunsch（内置）
- **打包**：PyInstaller

## License

MIT License — 详见 [LICENSE](LICENSE)

## Acknowledgements

- [MAFFT](https://mafft.cbrc.jp/alignment/software/) — 多序列比对算法
- [Flask](https://flask.palletsprojects.com/) — Python Web 框架

## v1.1.0 Changelog

**Stability & Accuracy Update**

- 序列合法性检查：非法字符检测
- FASTA 解析增强：多行序列、空行、重复 header
- GAP 统计准确性修正
- 差异位置映射：Alignment Position ↔ Sequence Position
- MAFFT 调用稳定性：方法名、timeout、输出解析
- 长序列可视化保护
- XSS 安全防护
