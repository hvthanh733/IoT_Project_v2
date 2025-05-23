# Reader.py
import csv
import os
from datetime import datetime
import sqlite3

# Thư mục chứa file CSV
LOG_FOLDER = "logs"

# Global max/min cho 4 block
global_stats = {
    i: {
        "max_temp": float("-inf"),
        "min_temp": float("inf"),
        "time_max_temp": None,
        "time_min_temp": None,
        "max_humi": float("-inf"),
        "min_humi": float("inf"),
        "time_max_humi": None,
        "time_min_humi": None
    } for i in range(1, 5)
}

def readLog():
    today = datetime.now().strftime("%Y%m%d")  # VD: "20250521"
    folder = os.path.join(LOG_FOLDER, today)

    if not os.path.exists(folder):
        print(f"[readLog] Folder not found: {folder}")
        return

    for block_id in range(1, 5):
        file_path = os.path.join(folder, f"block{block_id}_data.csv")
        if not os.path.exists(file_path):
            print(f"[readLog] File not found: {file_path}")
            continue

        try:
            with open(file_path, "r") as f:
                reader = list(csv.DictReader(f))
                if not reader:
                    continue
                last_row = reader[-1]
        except Exception as e:
            print(f"[readLog] Failed to read {file_path}: {e}")
            continue

        try:
            # Lấy dữ liệu từ dòng cuối cùng
            temp = float(last_row["temperature"])
            humi = float(last_row["humidity"])
            fire = int(last_row["fire_state"])
            timestamp_str = last_row["time_stemp"]
            datetime = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            time = datetime.strptime(timestamp_str, "%H%M%S")
            stats = global_stats[block_id]

            # Cập nhật max/min temp
            if temp > stats["max_temp"]:
                stats["max_temp"] = temp
                stats["time_max_temp"] = time
            if temp < stats["min_temp"]:
                stats["min_temp"] = temp
                stats["time_min_temp"] = time

            # Cập nhật max/min humi
            if humi > stats["max_humidity"]:
                stats["max_humidity"] = humi
                stats["time_max_humi"] = time
            if humi < stats["min_humidity"]:
                stats["min_humidity"] = humi
                stats["time_min_humi"] = time
            if
            # Ghi vào DB
            write2Database(
                block_id,
                temp,
                stats["max_temp"],
                stats["min_temp"],
                stats["time_max_temp"],
                stats["time_min_temp"],
                humi,
                stats["max_humidity"],
                stats["min_humidity"],
                stats["time_max_humi"],
                stats["time_min_humi"],
                fire,
                None,   # time_start (tùy hệ thống cháy)
                None    # total_time
            )

        except Exception as e:
            print(f"[readLog] ❌ Error parsing row: {e}")



def write2Database(block_id, temp, max_temp, min_temp, time_max_temp, time_min_temp,
                   do_am, do_am_max, do_am_min, time_max_humi, time_min_humi,
                   fire_state, time_start, total_time):
    conn = sqlite3.connect("iot_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO sensor_data (
            block_id, date,
            max_temp, min_temp, time_max_temp, time_min_temp,
            do_am_max, do_am_min, time_max_humi, time_min_humi,
            fire_state, start_time, end_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        block_id, date,
        max_temp, min_temp, time_max_temp, time_min_temp,
        max_humi, min_humi, time_max_humi, time_min_humi,
        fire_state, start_time, end_time
    ))

    conn.commit()
    conn.close()
    print(f"[write2Database] ✅ Block {block_id} inserted.")
