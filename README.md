# OpenCode Paddle-OCR Skill

> 🔍 让无视觉能力的大模型也能"看"图片 — OpenCode/OpenWork AI OCR Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenCode](https://img.shields.io/badge/OpenCode-Skill-blue)](https://opencode.ai)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR--VL-0.9B-green)](https://ollama.com/MedAIBase/PaddleOCR-VL)

## 简介

这是一个 **OpenCode/OpenWork** 的 OCR Skill，使用百度 **PaddleOCR-VL 0.9B** 模型通过 Ollama 本地部署，为无视觉能力的大模型（如 GLM-4.7）提供图像识别能力。

### 特性

- ✅ **超轻量**: 仅 0.9B 参数，CPU 可运行
- ✅ **多语言**: 支持 109 种语言
- ✅ **多格式**: 图片 (PNG/JPG/BMP/GIF/WEBP) + PDF
- ✅ **复杂识别**: 表格、公式、图表
- ✅ **本地运行**: 完全离线，数据安全
- ✅ **性能第一**: OmniDocBench V1.5 全球排名 #1

## 工作原理

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ 图片/PDF    │────▶│ PaddleOCR-VL     │────▶│ 主模型分析      │
│             │     │ (本地 Ollama)    │     │ (GLM-4.7 等)    │
└─────────────┘     └──────────────────┘     └─────────────────┘
```

## 快速开始

### 1. 安装环境

```bash
# 安装 Ollama
brew install ollama

# 启动服务
brew services start ollama

# 下载模型 (约 935MB)
ollama pull MedAIBase/PaddleOCR-VL:0.9b

# 安装 Python 依赖
pip install requests pdf2image
brew install poppler
```

### 2. 安装 Skill

```bash
# 克隆到 OpenWork Skills 目录
cd ~/Library/Application\ Support/com.differentai.openwork/workspaces/starter/.opencode/skills
git clone https://github.com/mr-shaper/opencode-skills-paddle-ocr.git paddle-ocr
```

### 3. 使用

```bash
cd paddle-ocr

# 图片 OCR
python3 scripts/ocr.py image.png

# PDF OCR
python3 scripts/ocr.py document.pdf

# 自定义提示
python3 scripts/ocr.py table.png --prompt "提取表格为 markdown"

# JSON 输出
python3 scripts/ocr.py image.png --json
```

## 目录结构

```
paddle-ocr/
├── SKILL.md              # OpenCode Skill 主文档
├── README.md             # GitHub 说明
├── 部署说明.md            # 详细部署指南
├── .gitignore
├── .env.example
└── scripts/
    ├── ocr.py            # 核心 OCR 脚本
    ├── setup_check.py    # 环境检查
    └── requirements.txt
```

## 环境检查

```bash
python3 scripts/setup_check.py
```

预期输出:
```
[OK] Ollama installed
[OK] Ollama server is running
[OK] PaddleOCR-VL model installed
[OK] Python dependencies
[OK] Poppler installed

All checks passed!
```

## Ollama 服务管理

```bash
# 查看状态
brew services list | grep ollama

# 启动
brew services start ollama

# 停止
brew services stop ollama

# 重启
brew services restart ollama
```

> 💡 空闲时 Ollama 仅占用 ~30MB 内存，模型只在调用时加载。

## 代码集成示例

```python
import subprocess
import json

# 调用 OCR
result = subprocess.run(
    ["python3", "scripts/ocr.py", "chart.png", "--json"],
    capture_output=True, text=True
)

# 解析结果
ocr_data = json.loads(result.stdout)
extracted_text = ocr_data["text"]

# 传给主模型
prompt = f"分析以下从图片提取的内容:\n{extracted_text}"
```

## 技术选型

| 对比项 | PaddleOCR-VL 0.9B | DeepSeek-OCR 3B |
|--------|-------------------|-----------------|
| 参数量 | **0.9B** ✅ | 3B |
| 显存需求 | CPU 可跑 ✅ | 8-16GB |
| 性能榜单 | #1 ✅ | 优秀 |
| macOS | 完美支持 ✅ | 支持 |

## 相关链接

- [PaddleOCR-VL on Ollama](https://ollama.com/MedAIBase/PaddleOCR-VL)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [OpenCode](https://opencode.ai)
- [Ollama](https://ollama.ai)

## License

MIT License

---

Made with ❤️ for OpenCode/OpenWork community
