import csv
import os
from datetime import datetime
import sqlite3

# Biến lưu trạng thái cũ
previous_temp = None
previous_humi = None

DB_PATH = "iot_system.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS button_alert (
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

    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])

    return file_path

# --- Ghi dữ liệu nếu có thay đổi ---
def SaveData(temperature, humidity, fire_status):
    global previous_temp, previous_humi

    file_path = makeFile()
    current_time = datetime.now().strftime("%H%M%S")

    if previous_temp is None or previous_humi is None or temperature != previous_temp or humidity != previous_humi:
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, temperature, humidity, fire_status])

        previous_temp = temperature
        previous_humi = humidity

        print(f"[Block 1] Ghi log: {temperature}°C - {humidity}% - {fire_status}")
    
def save_event(note):
    now = datetime.now()
    date = now.strftime("2026-07-08")
    time_start = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO button_alert (date, time_start, time_end, note)
        VALUES (?, ?, ?, ?)
    """, (date, time_start, None, note))
    conn.commit()
    conn.close()

    print(f"URAAAAA Đã lưu với note: {note} {date} {time_start}")



# # --- Hàm lưu dữ liệu ---
# def saveData(temperature, humidity, fire_status, block_number):
#     file_path = makeFile(block_number)
#     current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

#     # Khởi tạo nếu block này chưa có
#     if block_number not in previous_data:
#         previous_data[block_number] = {}
#         temp_his[block_number] = {"temp": set(), "humi": set()}
#         fire_state_queue[block_number] = deque(maxlen=2)
#         is_fire_active[block_number] = False

#     was_fire = is_fire_active[block_number]
#     should_save = False

#     # --- Xử lý nhiệt độ ---
#     temp_changed = False
#     if temperature is not None:
#         prev_temp = previous_data[block_number].get("temp")
#         if temperature != prev_temp and temperature not in temp_his[block_number]["temp"]:
#             previous_data[block_number]["temp"] = temperature
#             temp_his[block_number]["temp"].add(temperature)
#             temp_changed = True
#             should_save = True

#     # --- Xử lý độ ẩm ---
#     humi_changed = False
#     if humidity is not None:
#         prev_humi = previous_data[block_number].get("humi")
#         if humidity != prev_humi and humidity not in temp_his[block_number]["humi"]:
#             previous_data[block_number]["humi"] = humidity
#             temp_his[block_number]["humi"].add(humidity)
#             humi_changed = True
#             should_save = True

#     # --- Xử lý lửa ---
#     fire_state_queue[block_number].append(fire_status)

#     # Nếu 2 lần liên tiếp đều Fire và trước đó chưa cháy -> bắt đầu cháy
#     if list(fire_state_queue[block_number]) == ["Fire", "Fire"] and not was_fire:
#         fire_status = "Fire"
#         is_fire_active[block_number] = True
#         should_save = True

#     # Nếu 2 lần liên tiếp đều No Fire và trước đó đang cháy -> kết thúc cháy
#     if list(fire_state_queue[block_number]) == ["No Fire", "No Fire"] and was_fire:
#         fire_status = "No Fire"
#         is_fire_active[block_number] = False
#         should_save = True

#     # Nếu đang cháy và nhiệt độ hoặc độ ẩm thay đổi cũng ghi lại
#     if was_fire and (temp_changed or humi_changed):
#         should_save = True
#         fire_status = "Fire"

#     # Nếu không có gì đặc biệt -> không ghi
#     if not should_save:
#         return

#     row = [current_time, round(temperature, 1), round(humidity, 1), fire_status]
#     print(f"Block {block_number} fire queue: {list(fire_state_queue[block_number])}, was_fire: {was_fire}, save as: {fire_status}")

#     with open(file_path, 'a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(row)
# 













# Nếu 1 giá trị lớn hơn threshold max min đã set up trước -> báo lỗi luôn
# def saveDataThreshold:

#     queue (liên tục lớn hơn X (Threshold đã set))
#     path = logs/threshold/ block{{i}}
#     định dạng
#     if queue:
#         1.tạo path

#         2.time_temp, nhiệt, ẩm, lửa như trên

#     Alert()

# def saveDataButton:
#     Alert()


# 1/
# 1. Bình thường cháy ví dụ 9:00:00 queue 2 cái là cháy hết -> ghi Fire
# 2. qeue 2 cái là ko cháy -> ghi No Fire
# -> tìm được thời gian bắt đầu, kết thúc
# Nếu có Fire -> Alert (): Có cháy

# 2/ 
# 4 block value
# ví dụ block 1 cháy:
# 9:00:00 30, 30, 0
# -> Case 2 threshod

# if button1: # Báo cháy
#     Alert()
#     mở path /logs/buttonAlert_1/date1/ ghi 9:00:00,30,30,0
#     ko ghi thời gian kết thúc
   
# if threshold:
#     Alert()
#     mở path /logs/threshold/date_1/ ghi 9:00:00,30,30,0
#     ko ghi thời gian kết thúc
# if not button and threshold()
#     SaveData


