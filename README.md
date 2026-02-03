# OpenCode Paddle-OCR Skill

> 让无视觉能力的大模型也能"看"图片 — OpenCode/OpenWork AI OCR Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenCode](https://img.shields.io/badge/OpenCode-Skill-blue)](https://opencode.ai)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-PP--OCRv5-green)](https://github.com/PaddlePaddle/PaddleOCR)

## 简介

这是一个 **OpenCode/OpenWork** 的 OCR Skill，使用 **PaddleOCR (PP-OCRv5)** 原生 Python 库，为无视觉能力的大模型（如 GLM-4.7）提供图像识别能力。

### 特性

- **超轻量**: ~200MB 模型文件，CPU 可运行
- **多语言**: 支持 100+ 种语言
- **多格式**: 图片 (PNG/JPG/BMP/GIF/WEBP/TIFF) + PDF
- **复杂识别**: 表格、公式、图表
- **本地运行**: 完全离线，数据安全
- **无服务依赖**: 不需要后台服务，按需加载

## 工作原理

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ 图片/PDF    │────▶│ PaddleOCR        │────▶│ 主模型分析      │
│             │     │ (本地 Python)    │     │ (GLM-4.7 等)    │
└─────────────┘     └──────────────────┘     └─────────────────┘
```

## 快速开始

### 1. 安装环境

```bash
# 安装 Python 依赖
pip install paddleocr paddlepaddle

# 安装 PDF 支持
pip install pdf2image
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

# 指定语言
python3 scripts/ocr.py image.png --lang en      # 英文
python3 scripts/ocr.py image.png --lang japan   # 日文

# JSON 输出
python3 scripts/ocr.py image.png --json

# 保存到文件
python3 scripts/ocr.py doc.pdf --output result.txt
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
[OK] PaddlePaddle installed
[OK] PaddleOCR installed
[OK] pdf2image installed
[OK] Pillow installed
[OK] Poppler installed
[OK] Model cache found

All checks passed!
```

## 资源占用

| 状态 | CPU | 内存 | 说明 |
|------|-----|------|------|
| **空闲时** | 0% | 0 | 不占用资源（按需加载） |
| **首次加载** | 高 | ~500MB | 加载模型到内存 |
| **推理时** | 中-高 | ~500MB-1GB | 处理图片时 |
| **处理完成** | 0% | 可释放 | 脚本退出后释放 |

### 模型文件

| 组件 | 大小 |
|------|------|
| PP-OCRv5 检测模型 | ~50MB |
| PP-OCRv5 识别模型 | ~100MB |
| 方向分类模型 | ~10MB |
| **总计** | **~200MB** |

> 模型自动缓存在 `~/.paddlex/official_models/`

## 代码集成示例

```python
import subprocess
import json

# 调用 OCR
result = subprocess.run(
    ["python3", "scripts/ocr.py", "chart.png", "--json"],
    capture_output=True, text=True,
    cwd="/path/to/paddle-ocr"
)

# 解析结果
ocr_data = json.loads(result.stdout)
extracted_text = ocr_data["text"]

# 传给主模型
prompt = f"分析以下从图片提取的内容:\n{extracted_text}"
```

## 常见问题

### 首次运行很慢？
首次运行需从 HuggingFace 下载模型（约 200MB），之后使用缓存。

### 网络问题无法下载模型？
```bash
export PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
python3 scripts/ocr.py image.png
```

### PDF 处理失败？
```bash
brew install poppler
pip install pdf2image
```

## 相关链接

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [PaddleOCR 官方文档](https://paddlepaddle.github.io/PaddleOCR/)
- [OpenCode](https://opencode.ai)

## License

MIT License

---

Made with ❤️ for OpenCode/OpenWork community
