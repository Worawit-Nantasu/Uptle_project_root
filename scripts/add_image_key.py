import json
import os
from datetime import datetime

INPUT_DIR = os.path.join("data", "input")
OUTPUT_DIR = os.path.join("data", "output")
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "script_run.log")
REVIEW_COUNT_FILE = os.path.join(LOG_DIR, "review_counts.json")


def add_image_key_to_all_files():
    # โหลดข้อมูลในโฟลเดอร์ input
    input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.json')]
    
    if not input_files:
        log_message("No JSON files found in input directory.")
        return

    for json_file in input_files:
        process_file(json_file)


def process_file(json_file):
    input_path = os.path.join(INPUT_DIR, json_file)
    output_path = os.path.join(OUTPUT_DIR, json_file)

    if not os.path.exists(input_path):
        log_message(f"ERROR: Input file {input_path} does not exist.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rating_schema = data.get("rating_schema", [])
    if not isinstance(rating_schema, list):
        log_message(f"WARNING: 'rating_schema' is not a list or doesn't exist in {json_file}.")
        rating_schema = []

    # แปลงชื่อไฟล์ (ตัดนามสกุล .json และแทนที่ - ด้วย _)
    base_name = os.path.splitext(json_file)[0].replace("-", "_")
    
    review_names = []
    for i, review in enumerate(rating_schema):
        review_image_name = f"{base_name}_review{i}"
        review["image"] = review_image_name
        review_names.append(review_image_name)
    
    # เขียนข้อมูลหลังแก้ไขลงไฟล์ output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # บันทึกข้อมูลรีวิวลงในไฟล์ review_counts.json
    save_review_list(review_names, json_file)
    
    log_message(f"SUCCESS: Added 'image' key to {len(review_names)} items in {json_file}.")


def save_review_list(review_list, filename):
    """
    บันทึกชื่อรีวิวทั้งหมดลงในไฟล์ review_counts.json ในรูปแบบ:
    {
      "<filename>": [
        "<base_name>_review0",
        "<base_name>_review1",
        ...
      ]
    }
    """
    if os.path.exists(REVIEW_COUNT_FILE):
        # ถ้าไฟล์มีอยู่แล้ว ให้โหลดขึ้นมาแก้ไขต่อ
        with open(REVIEW_COUNT_FILE, "r", encoding="utf-8") as f:
            review_data = json.load(f)
    else:
        # ถ้าไม่มีไฟล์ ให้สร้าง dict ว่าง
        review_data = {}
    
    review_data[filename] = review_list
    
    # เขียนข้อมูลกลับลงไฟล์
    with open(REVIEW_COUNT_FILE, "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_f:
        log_f.write(f"[{timestamp}] {message}\n")


if __name__ == "__main__":
    add_image_key_to_all_files()
