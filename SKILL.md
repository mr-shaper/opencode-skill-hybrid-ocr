---
name: paddle-ocr
description: |
  Lightweight OCR skill using PaddleOCR-VL (0.9B) via Ollama for text extraction from images and PDFs.
  Supports 109 languages, tables, formulas, and charts.
  Use when: "OCR this image", "extract text from image/PDF", "read document content", "recognize text", "parse document"
---

# PaddleOCR-VL OCR Skill

## Overview

This skill provides OCR (Optical Character Recognition) capabilities using the PaddleOCR-VL 0.9B model through Ollama. It enables text extraction from images and PDFs, with support for:

- **109 languages** including Chinese, English, Japanese, Korean, etc.
- **Complex elements**: Tables, mathematical formulas, charts
- **Multiple formats**: PNG, JPG, PDF, BMP, GIF, WEBP

## Quick Start

### Single Image OCR
```bash
python scripts/ocr.py image.png
```

### PDF Document OCR
```bash
python scripts/ocr.py document.pdf
```

### Custom Prompt (Table Extraction)
```bash
python scripts/ocr.py table.png --prompt "Extract the table data and format as markdown"
```

### JSON Output
```bash
python scripts/ocr.py image.png --json > result.json
```

### Save to File
```bash
python scripts/ocr.py document.pdf --output extracted_text.txt
```

## Integration with Non-Vision Models

This skill is designed to give image analysis capabilities to models that cannot process images directly (like GLM-4.7, text-only models, etc.).

### Workflow
```
Image/PDF → PaddleOCR-VL (Ollama) → Extracted Text → Main Model Analysis
```

### Example Integration
```python
import subprocess
import json

# Step 1: Extract text from image
result = subprocess.run(
    ["python3", "scripts/ocr.py", "chart.png", "--json"],
    capture_output=True, text=True
)
ocr_result = json.loads(result.stdout)
extracted_text = ocr_result["text"]

# Step 2: Pass to main model for analysis
prompt = f"""
Based on the following OCR-extracted content:

{extracted_text}

Please analyze the data and provide insights.
"""
```

## Common Use Cases

### 1. Document Digitization
```bash
python scripts/ocr.py scanned_document.pdf --output document.txt
```

### 2. Table Data Extraction
```bash
python scripts/ocr.py spreadsheet.png --prompt "Extract the table as CSV format"
```

### 3. Formula Recognition
```bash
python scripts/ocr.py math_problem.jpg --prompt "Extract mathematical formulas in LaTeX format"
```

### 4. Chart Data Extraction
```bash
python scripts/ocr.py bar_chart.png --prompt "Extract the data values from this chart"
```

### 5. Multi-language Document
```bash
python scripts/ocr.py chinese_document.png  # Automatically detects language
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `PADDLEOCR_MODEL` | `MedAIBase/PaddleOCR-VL:0.9b` | Model to use |

## First-Time Setup

### 1. Install Ollama
```bash
brew install ollama
```

### 2. Start Ollama Server
```bash
brew services start ollama
# or: ollama serve
```

### 3. Pull PaddleOCR-VL Model
```bash
ollama pull MedAIBase/PaddleOCR-VL:0.9b
```

### 4. Install Python Dependencies
```bash
pip install requests pdf2image
```

### 5. Install Poppler (for PDF support)
```bash
brew install poppler
```

### 6. Verify Setup
```bash
python scripts/setup_check.py
```

## Troubleshooting

### "Cannot connect to Ollama"
```bash
# Ensure Ollama is running
brew services start ollama
# or
ollama serve
```

### "Model not found"
```bash
ollama pull MedAIBase/PaddleOCR-VL:0.9b
```

### "pdf2image error"
```bash
brew install poppler
pip install pdf2image
```

### Slow Performance
- PaddleOCR-VL runs on CPU on macOS (still fast for 0.9B model)
- Large images may take 10-30 seconds
- Consider resizing very large images before processing

## Model Information

| Property | Value |
|----------|-------|
| Model | PaddleOCR-VL 0.9B |
| Size | 935 MB |
| Context | 128K tokens |
| Languages | 109 |
| Source | [Ollama Hub](https://ollama.com/MedAIBase/PaddleOCR-VL) |

## See Also

- [PDF Skill](../pdf/SKILL.md) - For PDF manipulation (merge, split, etc.)
- [DOCX Skill](../docx/SKILL.md) - For Word document operations
