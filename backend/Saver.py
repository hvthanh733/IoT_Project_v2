import csv
import os
from datetime import datetime
import sqlite3

# Biến lưu trạng thái cũ
previous_temp = None
previous_humi = None
# 100 Lines equal 16-18Kb
MAX_LINES = 200
DB_PATH = "iot_system.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fire_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()


# --- Tạo file nếu chưa tồn tại ---
def makeFile():
    today = datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join("logs", today)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "block1_data.csv")

    try:
        if not os.path.exists(file_path):
            # Nếu file không tồn tại, tạo mới luôn
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
        else:
            # Kiểm tra số dòng, nếu vượt MAX_LINES thì xóa và tạo lại
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            if lines >= MAX_LINES:
                os.remove(file_path)
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
    except Exception as e:
        print(f"Lỗi trong makeFile: {e}")

    return file_path

# def makeFile():
#     today = datetime.now().strftime("%Y%m%d")
#     folder_path = os.path.join("logs", today)
#     os.makedirs(folder_path, exist_ok=True)

#     file_path = os.path.join(folder_path, "block1_data.csv")

#     if not os.path.exists(file_path):
#         with open(file_path, 'w', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
#     else:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             lines = sum(1 for _ in f)
#         if lines >= MAX_LINES:
#             os.remove(file_path)
#             with open(file_path, 'w', newline='', encoding='utf-8') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
#     return file_path


last_data = {"temperature": None, "humidity": None, "fire_state": None}  # Theo dõi dữ liệu cũ
def saveDataFromSTM32(temperature, humidity, fire_state):
    file_path = makeFile()

    # Ghi dữ liệu mới vào CSV (không kiểm tra trùng lặp)
    time_stamp = datetime.now().strftime("%H:%M:%S")
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time_stamp, temperature, humidity, fire_state])
# def saveDataFromSTM32(temperature, humidity, fire_state):
#     file_path = makeFile()
    
#     if os.path.exists(file_path):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 try:
#                     temp = float(row["temperature"])
#                     humi = float(row["humidity"])
#                 except ValueError:
#                     continue
#                 if temp == temperature and humi == humidity:
#                     return

#     time_stamp = datetime.now().strftime("%H:%M:%S")
#     with open(file_path, 'a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow([time_stamp, temperature, humidity, fire_state])
def delete_csv_file():
    today = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join("logs", today, "block1_data.csv")

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Đã xóa: {file_path}")
        except Exception as e:
            print(f"Lỗi khi xóa file: {e}")
    else:
        print(f"File không tồn tại: {file_path}")

def readCSV():
    today = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join("logs", today, "block1_data.csv")
    print("file_path", file_path)
    if not os.path.exists(file_path):
        return None

    max_temp = None
    time_max_temp = None
    min_humi = None
    time_min_humi = None
    fire_states = []

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                temp = float(row["temperature"])
                humi = float(row["humidity"])
                fire = int(float(row["fire_state"]))
                time = row["time_stemp"]
            except (ValueError, KeyError):
                continue

            if max_temp is None or temp > max_temp:
                max_temp = temp
                time_max_temp = time

            if min_humi is None or humi < min_humi:
                min_humi = humi
                time_min_humi = time

            fire_states.append(fire)

    if max_temp is None or min_humi is None:
        return None

    fire_detected = 0 if 0 in fire_states else 1

    return (
        max_temp,
        time_max_temp,
        # min_humi,
        # time_min_humi,
        # fire_detected
    )
