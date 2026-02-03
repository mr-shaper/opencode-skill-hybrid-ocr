#!/usr/bin/env python3
"""
PaddleOCR-VL OCR Script
Supports: Images (PNG, JPG, JPEG, BMP, GIF, WEBP, TIFF) and PDFs
Uses Ollama API to call MedAIBase/PaddleOCR-VL:0.9b
"""

import argparse
import base64
import json
import os
import sys
import tempfile
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# Configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.environ.get("PADDLEOCR_MODEL", "MedAIBase/PaddleOCR-VL:0.9b")

# Supported file extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tiff", ".tif"}
PDF_EXTENSION = ".pdf"


def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def pdf_to_images(pdf_path: str) -> list:
    """Convert PDF pages to temporary image files."""
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image not found. Install with: pip install pdf2image", file=sys.stderr)
        print("Also ensure poppler is installed: brew install poppler", file=sys.stderr)
        sys.exit(1)

    try:
        images = convert_from_path(pdf_path, dpi=200)
    except Exception as e:
        print(f"Error converting PDF: {e}", file=sys.stderr)
        print("Ensure poppler is installed: brew install poppler", file=sys.stderr)
        sys.exit(1)

    temp_paths = []

    for i, image in enumerate(images):
        temp_file = tempfile.NamedTemporaryFile(
            suffix=".png", delete=False, prefix=f"page_{i+1}_"
        )
        image.save(temp_file.name, "PNG")
        temp_paths.append(temp_file.name)
        print(f"Converted page {i+1}/{len(images)} to temporary image", file=sys.stderr)

    return temp_paths


def call_ollama_ocr(image_path: str, prompt: str = None) -> str:
    """Call Ollama API with image for OCR."""

    if prompt is None:
        prompt = (
            "Please perform OCR on this image and extract all text content. "
            "Preserve the original layout and formatting as much as possible. "
            "For tables, output them in markdown format. "
            "For formulas, output them in LaTeX format."
        )

    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_base64]
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=180  # 3 minutes for large images
        )
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "")
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to Ollama at {OLLAMA_BASE_URL}", file=sys.stderr)
        print("Please ensure Ollama is running: ollama serve", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out. The image might be too large.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        if "model" in str(e).lower():
            print(f"Model may not be installed. Run: ollama pull {MODEL_NAME}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error calling Ollama API: {e}", file=sys.stderr)
        sys.exit(1)


def process_image(image_path: str, prompt: str = None) -> dict:
    """Process a single image and return OCR result."""
    print(f"Processing image: {image_path}", file=sys.stderr)
    result = call_ollama_ocr(image_path, prompt)

    return {
        "source": str(image_path),
        "type": "image",
        "text": result
    }


def process_pdf(pdf_path: str, prompt: str = None) -> dict:
    """Process a PDF file by converting to images and OCR each page."""
    print(f"Processing PDF: {pdf_path}", file=sys.stderr)
    temp_images = pdf_to_images(pdf_path)

    pages = []
    try:
        for i, image_path in enumerate(temp_images):
            print(f"OCR processing page {i+1}/{len(temp_images)}...", file=sys.stderr)
            result = call_ollama_ocr(image_path, prompt)
            pages.append({
                "page": i + 1,
                "text": result
            })
    finally:
        # Cleanup temporary files
        for temp_path in temp_images:
            try:
                os.unlink(temp_path)
            except Exception:
                pass

    return {
        "source": str(pdf_path),
        "type": "pdf",
        "total_pages": len(pages),
        "pages": pages
    }


def format_output(result: dict, as_json: bool = False) -> str:
    """Format the OCR result for output."""
    if as_json:
        return json.dumps(result, indent=2, ensure_ascii=False)

    if result.get("type") == "pdf":
        # PDF output - combine all pages
        parts = []
        for page in result.get("pages", []):
            parts.append(f"=== Page {page['page']} ===\n{page['text']}")
        return "\n\n".join(parts)
    else:
        # Image output
        return result.get("text", "")


def main():
    parser = argparse.ArgumentParser(
        description="OCR using PaddleOCR-VL via Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ocr.py image.png                    # OCR a single image
  python ocr.py document.pdf                 # OCR all pages of a PDF
  python ocr.py image.png --json             # Output as JSON
  python ocr.py image.png --prompt "提取表格数据"  # Custom prompt (Chinese)
  python ocr.py doc.pdf -o result.txt        # Save to file

Supported formats:
  Images: PNG, JPG, JPEG, BMP, GIF, WEBP, TIFF
  Documents: PDF
        """
    )
    parser.add_argument("input_file", help="Image or PDF file to process")
    parser.add_argument("--prompt", "-p", help="Custom prompt for OCR")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    # Determine file type
    suffix = input_path.suffix.lower()

    if suffix == PDF_EXTENSION:
        result = process_pdf(str(input_path), args.prompt)
    elif suffix in IMAGE_EXTENSIONS:
        result = process_image(str(input_path), args.prompt)
    else:
        print(f"Error: Unsupported file type: {suffix}", file=sys.stderr)
        print(f"Supported: PDF, {', '.join(sorted(IMAGE_EXTENSIONS))}", file=sys.stderr)
        sys.exit(1)

    # Format output
    output_text = format_output(result, args.json)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"Output saved to: {args.output}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
