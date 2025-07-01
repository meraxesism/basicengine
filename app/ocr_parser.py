import os
import json
import re
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# ✅ Hardcoded paths so no PATH setup needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"  # Or just \bin if you installed directly

# Folders
UPLOAD_DIR = "data/uploads"
IMAGE_DIR = "data/images"
OUTPUT_JSON = "data/chunks.json"
DPI = 300  # high-quality OCR

# Make sure folders exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def extract_pdf_data_ocr(pdf_path):
    dtc_pattern = re.compile(r"^U\d{4}.*", re.IGNORECASE)
    chunks = []
    current_chunk = None

    # Step 1: Convert PDF pages to images
    print("🖼️ Converting PDF pages to images...")
    pages = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)

    # Step 2: OCR each page
    for page_num, image in enumerate(pages):
        print(f"🔍 OCR on Page {page_num + 1}")
        text = pytesseract.image_to_string(image)

        # Save image for flowchart option
        img_name = f"page{page_num + 1}.png"
        image.save(os.path.join(IMAGE_DIR, img_name))

        # Step 3: Split into DTC chunks (U0101, U0140, etc.)
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if dtc_pattern.match(line):
                if current_chunk:
                    chunks.append(current_chunk)

                current_chunk = {
                    "page": page_num + 1,
                    "text": line,
                    "images": [img_name]
                }
            elif current_chunk:
                current_chunk["text"] += "\n" + line

    # Add last chunk
    if current_chunk:
        chunks.append(current_chunk)

    # Step 4: Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"✅ OCR extracted {len(chunks)} DTC sections.")
    return chunks
