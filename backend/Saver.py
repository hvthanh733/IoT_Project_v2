import csv
import os
from datetime import datetime

# 100 Lines equal 8-9Kb
MAX_LINES = 100  # Include header

# Make file block{numbder}_data.csvs
def makeFile(block_number):
    today = datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join("logs", today)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"block{block_number}_data.csv")

    # Nếu file chưa tồn tại, tạo mới và ghi header
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
    else:
        # Nếu file đã tồn tại, kiểm tra số dòng
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f)
        if lines >= MAX_LINES:
            # Xóa file cũ
            os.remove(file_path)
            # Tạo mới và ghi header
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])

    return file_path

def saveData(temperature, humidity, fire_status, block_number):
    file_path = makeFile(block_number)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    row = [current_time, round(temperature, 1), round(humidity, 1), fire_status]

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)


