# SeqDiff Visualizer

**v1.1 — Stability & Accuracy Update**

一个用于 DNA 双序列比对、差异率分析与差异位点可视化的轻量工具，支持 NW 和 MAFFT 两种自动比对方式，以及多种 GAP 处理策略，并提供序列裁剪、差异位置映射和结果导出功能。

特别适用于需要比较不同 GAP 处理策略对序列差异率影响的场景。

---

## Screenshots

| Input | Results |
| :---: | :---: |
| ![Input](./docs/screenshots/1-input.png) | ![Results](./docs/screenshots/2-result.png) |

---

## Features

- **DNA 双序列比对**
  - 预比对模式（Pre-aligned）：直接比较已比对好的序列
  - Needleman-Wunsch 自动比对
  - MAFFT 自动比对（本地调用）
- **GAP 处理策略**
  - 支持 gap-open 和 gap-extension 参数
  - 可比较不同 GAP 处理对差异率的影响
- **差异率统计**
  - Alignment length / Identical sites / Mismatch sites / Gap sites
  - Identity / Mismatch rate / Gap rate
  - Variable sites
- **差异位置映射**
  - Alignment Position
  - Sequence 1 Position
  - Sequence 2 Position
- **差异表与导出**
  - 差异位点列表（含位置映射）
  - 复制差异结果
  - CSV 导出
- **序列裁剪**
  - 支持连续裁剪前后
  - 裁剪后自动更新统计与可视化
- **输入支持**
  - FASTA / TXT 文件上传
  - 文本框直接粘贴
- **界面功能**
  - 中文 / English 双语切换
  - 碱基着色（A/T/C/G）
  - 折行 / 单行显示切换
  - 悬停显示位点信息
  - 历史记录（最多 5 条）
- **Windows 绿色免安装版本**
- **长序列可视化保护**

## Quick Start

### Windows 用户（推荐）

💻 **下载绿色免安装包，已内置 MAFFT，解压后即可使用，无需安装 Python、Flask 或额外配置环境变量。**

1. 从 [Releases](https://github.com/Qianmoss/seq-diff-visualizer/releases) 下载 `SeqDiff.zip`
2. 解压到任意目录
3. 双击 `SeqDiff.exe`
4. 浏览器自动打开 http://localhost:5000

### Mac / Linux 用户

🐧 **需要自行准备 Python 环境，并安装 MAFFT。**

1. 安装 [Python 3.12](https://www.python.org/downloads/)
2. 安装 Flask：
   ```bash
   pip install flask
   ```
3. 下载 [MAFFT](https://mafft.cbrc.jp/alignment/software/)，解压到项目根目录的 `mafft-win` 文件夹
4. 运行：
   ```bash
   python app.py
   ```
5. 浏览器自动打开 http://localhost:5000

## Usage

1. **添加序列**：在文本框粘贴两条序列（支持 FASTA 格式），或点击上传文件
2. **选择模式**：Pre-aligned / NW Auto / MAFFT
3. **开始计算**：点击「Start」查看差异位点、统计与可视化

## Performance

⚡ **性能说明**

- **≤ 3000 bp：** 使用完整的逐位可视化，性能良好。
- **3000–5000 bp：** 正常分析和可视化，但会提示序列较长，可能影响浏览器渲染性能。
- **> 5000 bp：** 自动切换为简化视图，以避免大量 DOM 元素导致浏览器卡顿。

超长序列仍可进行比对和统计分析，仅可视化方式会进行简化。

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
│   └── screenshots/    # 项目截图
├── mafft-win/          # Windows 版 MAFFT（需自行下载）
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

## v1.1 更新说明

**v1.1 — Stability & Accuracy Update**

本次更新主要提升了数据可靠性与使用稳定性：

- 序列合法性检查：非法字符检测，不再静默删除
- FASTA 解析增强：支持多行序列、空行、重复 header
- GAP 统计准确性修正
- 差异位置映射：区分 Alignment Position 与 Sequence Position
- MAFFT 调用稳定性：方法名修正、timeout 统一、输出解析改进
- 长序列可视化保护：超过 5000 bp 自动简化视图
- 安全性：XSS 防护
