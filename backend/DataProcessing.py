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
        "time_min_humi": None,
        "fire_state": None,
        "fire_state_human": None,
        "start_time": None,
        "end_time": None,
    } for i in range(1, 5)
}

# Global fire detect array & flags
fire_array = {i: [] for i in range(1, 5)}
flag = {i: False for i in range(1, 5)}

def readLog():
    day_time = datetime.now().strftime("%Y%m%d")  # VD: "20250524"
    folder = os.path.join(LOG_FOLDER, day_time)
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
            timestamp_str = last_row["time_stemp"]  # Ví dụ: "20250524_154812"
            dt_obj = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            date_str = dt_obj.date().isoformat()    # '2025-05-24'
            time_str = dt_obj.time().isoformat()    # '15:48:12'

            stats = global_stats[block_id]
            stats["fire_state_human"] = 0

            # Cập nhật max/min nhiệt độ
            if temp > stats["max_temp"]:
                stats["max_temp"] = temp
                stats["time_max_temp"] = time_str
            if temp < stats["min_temp"]:
                stats["min_temp"] = temp
                stats["time_min_temp"] = time_str

            # Cập nhật max/min độ ẩm
            if humi > stats["max_humi"]:
                stats["max_humi"] = humi
                stats["time_max_humi"] = time_str
            if humi < stats["min_humi"]:
                stats["min_humi"] = humi
                stats["time_min_humi"] = time_str

            # Cập nhật lửa
            if fire == 1:
                if not flag[block_id]:
                    stats["start_time"] = time_str
                    stats["fire_state"] = 1
                    flag[block_id] = True
                fire_array[block_id] = []  # reset
            else:
                if flag[block_id]:
                    fire_array[block_id].append(0)
                    if len(fire_array[block_id]) >= 20:
                        stats["end_time"] = time_str
                        stats["fire_state"] = 0
                        flag[block_id] = False

            # Ghi DB (chỉ test, sau này nên có điều kiện trigger riêng)
            write2Database(
                block_id, date_str,
                stats["max_temp"], stats["min_temp"],
                stats["time_max_temp"], stats["time_min_temp"],
                stats["max_humi"], stats["min_humi"],
                stats["time_max_humi"], stats["time_min_humi"],
                stats["fire_state"], stats["fire_state_human"],
                stats["start_time"], stats["end_time"]
            )

        except Exception as e:
            print(f"[readLog] ❌ Error parsing row: {e}")


def insertData(block_id, date,
               max_temp, min_temp, time_max_temp, time_min_temp,
               max_humi, min_humi, time_max_humi, time_min_humi,
               fire_state, fire_state_human,
               start_time, end_time, cursor):
    cursor.execute('''
        INSERT INTO sensor_block_data (
            block_id, date,
            max_temp, min_temp, time_max_temp, time_min_temp,
            max_humi, min_humi, time_max_humi, time_min_humi,
            fire_state, fire_state_human,
            start_time, end_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        block_id, date,
        max_temp, min_temp, time_max_temp, time_min_temp,
        max_humi, min_humi, time_max_humi, time_min_humi,
        fire_state, fire_state_human,
        start_time, end_time
    ))
    print(f"[insertData] ✅ Block {block_id} inserted.")


def updateData(block_id, date,
               max_temp, min_temp, time_max_temp, time_min_temp,
               max_humi, min_humi, time_max_humi, time_min_humi,
               fire_state, fire_state_human,
               start_time, end_time, cursor):
    cursor.execute('''
        UPDATE sensor_block_data SET
            max_temp = ?,
            min_temp = ?,
            time_max_temp = ?,
            time_min_temp = ?,
            max_humi = ?,
            min_humi = ?,
            time_max_humi = ?,
            time_min_humi = ?,
            fire_state = ?,
            fire_state_human = ?,
            start_time = ?,
            end_time = ?
        WHERE block_id = ? AND date = ?
    ''', (
        max_temp, min_temp, time_max_temp, time_min_temp,
        max_humi, min_humi, time_max_humi, time_min_humi,
        fire_state, fire_state_human,
        start_time, end_time,
        block_id, date
    ))
    print(f"[updateData] 🔁 Block {block_id} updated.")


def write2Database(block_id, date,
                   max_temp, min_temp, time_max_temp, time_min_temp,
                   max_humi, min_humi, time_max_humi, time_min_humi,
                   fire_state, fire_state_human,
                   start_time, end_time):
    conn = sqlite3.connect("iot_system.db")
    cursor = conn.cursor()

    # Kiểm tra đã có dòng dữ liệu block_id + date chưa
    cursor.execute('''
        SELECT id FROM sensor_block_data WHERE block_id = ? AND date = ?
    ''', (block_id, date))
    result = cursor.fetchone()

    if result:
        updateData(block_id, date,
                   max_temp, min_temp, time_max_temp, time_min_temp,
                   max_humi, min_humi, time_max_humi, time_min_humi,
                   fire_state, fire_state_human,
                   start_time, end_time, cursor)
    else:
        insertData(block_id, date,
                   max_temp, min_temp, time_max_temp, time_min_temp,
                   max_humi, min_humi, time_max_humi, time_min_humi,
                   fire_state, fire_state_human,
                   start_time, end_time, cursor)

    conn.commit()
    conn.close()
