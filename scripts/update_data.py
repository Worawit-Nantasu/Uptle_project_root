import json
import os
from datetime import datetime

INPUT_DIR = os.path.join("data", "input")
OUTPUT_DIR = os.path.join("data", "output")
LOG_FILE = os.path.join("logs", "script_run.log")

INPUT_FILE = "google-search-ads-360.json"
OUTPUT_FILE = "google-search-ads-360.json"


def update_data():
    """
    ตัวอย่างสคริปต์สำหรับทำการอัพเดตข้อมูลเพิ่มเติม
    ในตัวอย่างนี้จะทำเป็นเพียงอ่านไฟล์แล้วเขียนกลับเฉยๆ
    แต่คุณสามารถเพิ่ม logic ตามต้องการ
    """
    input_path = os.path.join(INPUT_DIR, INPUT_FILE)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    if not os.path.exists(input_path):
        log_message(f"ERROR: Input file {input_path} does not exist.")
        return
    
    # โหลด JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # เพิ่มการปรับแต่ง/อัพเดตข้อมูลที่นี่
    # ตัวอย่าง: เพิ่มฟิลด์ "updated": True ใน root
    data["updated"] = True

    # เขียนกลับไปที่ output
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    log_message(f"SUCCESS: Updated data in {OUTPUT_FILE}.")


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_f:
        log_f.write(f"[{timestamp}] {message}\n")


if __name__ == "__main__":
    update_data()
