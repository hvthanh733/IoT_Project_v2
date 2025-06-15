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


# # --- Ghi dữ liệu nếu có thay đổi ---
# def SaveData(temperature, humidity, fire_status):
#     global previous_temp, previous_humi

#     file_path = makeFile()
#     current_time = datetime.now().strftime("%H%M%S")

#     if previous_temp is None or previous_humi is None or temperature != previous_temp or humidity != previous_humi:
#         with open(file_path, 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow([current_time, temperature, humidity, fire_status])

#         previous_temp = temperature
#         previous_humi = humidity

#         print(f"[Block 1] Ghi log: {temperature}°C - {humidity}% - {fire_status}")

# def save_event(note, end=False):
#     now = datetime.now()
#     date = now.strftime("%Y-%m-%d")
#     current_time = now.strftime("%H:%M:%S")

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     if end:
#         # Truy xuất dòng mới nhất có time_end IS NULL
#         cursor.execute("""
#             SELECT id, note FROM button_alert
#             WHERE time_end IS NULL
#             ORDER BY id DESC LIMIT 1
#         """)
#         last = cursor.fetchone()
#         if last:
#             last_id, last_note = last

#             # Phân biệt loại để sửa note
#             if "Khẩn cấp" in last_note:
#                 updated_note = last_note.strip() + " (Đã tắt bởi người dùng)"
#             elif "Cảnh báo" in last_note or "Nguy hiểm" in last_note:
#                 updated_note = last_note.strip() + " (Đã tắt bởi người dùng)"
#             else:
#                 updated_note = last_note.strip() + " (Đã kết thúc)"

#             # Cập nhật dòng đó
#             cursor.execute("""
#                 UPDATE button_alert
#                 SET time_end = ?, note = ?
#                 WHERE id = ?
#             """, (current_time, updated_note, last_id))

#             print(f"[UPDATE] Cập nhật dòng ID {last_id}: {updated_note} @ {current_time}")
#         else:
#             print("[WARNING] Không tìm thấy cảnh báo nào để cập nhật!")

#     else:
#         # Thêm dòng mới
#         cursor.execute("""
#             INSERT INTO button_alert (date, time_start, time_end, note)
#             VALUES (?, ?, ?, ?)
#         """, (date, current_time, None, note))

#         print(f"[SAVE] Lưu sự kiện mới: {note} @ {current_time}")

#     conn.commit()
#     conn.close()

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


