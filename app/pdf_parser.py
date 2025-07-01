import pdfplumber
import os
import json
import re
from collections import defaultdict

UPLOAD_DIR = "data/uploads"
OUTPUT_JSON = "data/chunks.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_pdf_data(pdf_path):
    dtc_pattern = re.compile(r"^U\d{4}.*", re.IGNORECASE)
    chunks = []
    current_chunk = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words()
            lines_by_y = defaultdict(list)

            # Group words by vertical position
            for word in words:
                if "x" not in word or "text" not in word:
                    continue
                y_key = round(word["top"] / 5) * 5
                lines_by_y[y_key].append(word)

            # Sort lines by y-position
            sorted_lines = sorted(lines_by_y.items())

            for _, words_in_line in sorted_lines:
                # Filter out any non-word elements
                valid_words = [w for w in words_in_line if "x" in w and "text" in w]

                if not valid_words:
                    continue

                line_text = " ".join([w["text"] for w in sorted(valid_words, key=lambda w: w["x"])])
                line_text = line_text.strip()

                if dtc_pattern.match(line_text):
                    if current_chunk:
                        chunks.append(current_chunk)

                    current_chunk = {
                        "page": page_num + 1,
                        "text": line_text,
                        "images": []
                    }
                elif current_chunk:
                    current_chunk["text"] += "\n" + line_text

    if current_chunk:
        chunks.append(current_chunk)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"✅ Extracted {len(chunks)} structured DTC chunks.")
    return chunks
