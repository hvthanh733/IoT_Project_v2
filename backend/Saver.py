
import csv
import os
from datetime import datetime
from collections import deque

previous_data = {}      # Lưu lần gần nhất đã ghi: { block_number: {"temp": ..., "humi": ...} }
temp_his = {}           # Ghi lại lịch sử từng giá trị đã ghi: { block_number: {"temp": set(), "humi": set()} }
fire_state_queue = {}   # Hàng đợi lưu 2 trạng thái gần nhất: { block_number: deque }
is_fire_active = {}     # Trạng thái hiện tại: đang cháy hay không

# --- Tạo file nếu chưa tồn tại ---
def makeFile(block_number):
    today = datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join("logs", today)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"block{block_number}_data.csv")

    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])

    return file_path

# --- Hàm lưu dữ liệu ---
def saveData(temperature, humidity, fire_status, block_number):
    file_path = makeFile(block_number)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Khởi tạo nếu block này chưa có
    if block_number not in previous_data:
        previous_data[block_number] = {}
        temp_his[block_number] = {"temp": set(), "humi": set()}
        fire_state_queue[block_number] = deque(maxlen=2)
        is_fire_active[block_number] = False

    was_fire = is_fire_active[block_number]
    should_save = False

    # --- Xử lý nhiệt độ ---
    temp_changed = False
    if temperature is not None:
        prev_temp = previous_data[block_number].get("temp")
        if temperature != prev_temp and temperature not in temp_his[block_number]["temp"]:
            previous_data[block_number]["temp"] = temperature
            temp_his[block_number]["temp"].add(temperature)
            temp_changed = True
            should_save = True

    # --- Xử lý độ ẩm ---
    humi_changed = False
    if humidity is not None:
        prev_humi = previous_data[block_number].get("humi")
        if humidity != prev_humi and humidity not in temp_his[block_number]["humi"]:
            previous_data[block_number]["humi"] = humidity
            temp_his[block_number]["humi"].add(humidity)
            humi_changed = True
            should_save = True

    # --- Xử lý lửa ---
    fire_state_queue[block_number].append(fire_status)

    # Nếu 2 lần liên tiếp đều Fire và trước đó chưa cháy -> bắt đầu cháy
    if list(fire_state_queue[block_number]) == ["Fire", "Fire"] and not was_fire:
        fire_status = "Fire"
        is_fire_active[block_number] = True
        should_save = True

    # Nếu 2 lần liên tiếp đều No Fire và trước đó đang cháy -> kết thúc cháy
    if list(fire_state_queue[block_number]) == ["No Fire", "No Fire"] and was_fire:
        fire_status = "No Fire"
        is_fire_active[block_number] = False
        should_save = True

    # Nếu đang cháy và nhiệt độ hoặc độ ẩm thay đổi cũng ghi lại
    if was_fire and (temp_changed or humi_changed):
        should_save = True
        fire_status = "Fire"

    # Nếu không có gì đặc biệt -> không ghi
    if not should_save:
        return

    row = [current_time, round(temperature, 1), round(humidity, 1), fire_status]
    print(f"Block {block_number} fire queue: {list(fire_state_queue[block_number])}, was_fire: {was_fire}, save as: {fire_status}")

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

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


