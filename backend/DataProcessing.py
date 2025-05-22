import os
import csv
import time
import sqlite3
from datetime import datetime

NUM_BLOCKS = 4
DATA_DIR = "logs"

# Biến cục bộ lưu giá trị max/min và thời gian
block_state = {}

for block_id in range(1, NUM_BLOCKS + 1):
    block_state[block_id] = {
        "max_temp": float('-inf'),
        "min_temp": float('inf'),
        "time_max_temp": None,
        "time_min_temp": None,
        "max_humi": float('-inf'),
        "min_humi": float('inf'),
        "time_max_humi": None,
        "time_min_humi": None,
        "fire_started": False,
        "time_start_fire": None,
        "total_fire_duration": 0.0
    }

def parse_bool(val):
    return bool(int(val))

def read_csv_and_update_state():
    today_str = datetime.now().strftime("%Y%m%d")

    for block_id in range(1, NUM_BLOCKS + 1):
        file_path = os.path.join(DATA_DIR, today_str, f"block{block_id}_data.csv")
        if not os.path.exists(file_path):
            continue

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 4:
                    continue

                try:
                    time_str, temp_str, humi_str, fire_str = row
                    temp = float(temp_str)
                    humi = float(humi_str)
                    fire = parse_bool(fire_str)
                    timestamp = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    continue

                state = block_state[block_id]

                # Nhiệt độ
                if temp > state["max_temp"]:
                    state["max_temp"] = temp
                    state["time_max_temp"] = timestamp
                if temp < state["min_temp"]:
                    state["min_temp"] = temp
                    state["time_min_temp"] = timestamp

                # Độ ẩm
                if humi > state["max_humi"]:
                    state["max_humi"] = humi
                    state["time_max_humi"] = timestamp
                if humi < state["min_humi"]:
                    state["min_humi"] = humi
                    state["time_min_humi"] = timestamp

                # Cháy
                if fire and not state["fire_started"]:
                    state["fire_started"] = True
                    if state["time_start_fire"] is None:
                        state["time_start_fire"] = timestamp

                elif not fire and state["fire_started"]:
                    # Kết thúc cháy
                    if state["time_start_fire"]:
                        duration = (timestamp - state["time_start_fire"]).total_seconds()
                        state["total_fire_duration"] += duration
                    state["fire_started"] = False
                    state["time_start_fire"] = None

def save_to_database():
    conn = sqlite3.connect("/home/thanh/Desktop/IoT_Project_v2/backend/iot_system.db")
    cursor = conn.cursor()

    for block_id in range(1, NUM_BLOCKS + 1):
        s = block_state[block_id]

        cursor.execute('''
            INSERT INTO sensor_data (
                block_id, max_temp, min_temp, time_max_temp, time_min_temp,
                do_am, do_am_max, do_am_min, time_max_humi, time_min_humi,
                fire_state, time_start, total_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            block_id,
            s["max_temp"],
            s["min_temp"],
            s["time_max_temp"].strftime("%Y-%m-%d %H:%M:%S") if s["time_max_temp"] else None,
            s["time_min_temp"].strftime("%Y-%m-%d %H:%M:%S") if s["time_min_temp"] else None,
            None,  # do_am hiện tại không lưu, có thể bổ sung nếu cần
            s["max_humi"],
            s["min_humi"],
            s["time_max_humi"].strftime("%Y-%m-%d %H:%M:%S") if s["time_max_humi"] else None,
            s["time_min_humi"].strftime("%Y-%m-%d %H:%M:%S") if s["time_min_humi"] else None,
            s["fire_started"],
            s["time_start_fire"].strftime("%Y-%m-%d %H:%M:%S") if s["time_start_fire"] else None,
            s["total_fire_duration"]
        ))

    conn.commit()
    conn.close()

def run_loop():
    while True:
        read_csv_and_update_state()
        save_to_database()
        time.sleep(5)  # Mỗi 5 giây lặp lại

if __name__ == "__main__":
    print("🚀 Đang chạy đọc và ghi dữ liệu sensor mỗi 5 giây...")
    run_loop()
