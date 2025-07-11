import sqlite3
import csv
import os
from datetime import datetime
from Saver import save_event
import time

def threshold_from_database(db_path="iot_system.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT threshold_temp_alert, threshold_humi_alert
            FROM sensor_block_property
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0], row[1]
        else:
            return None, None

    except Exception as e:
        print("Lỗi khi truy vấn threshold:", e)
        return None, None

def read_extreme_from_log():
    today = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join("logs", today, "block1_data.csv")

    max_temp = None
    min_humi = None

    if not os.path.exists(file_path):
        print("File log không tồn tại:", file_path)
        return None, None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    temp = float(row["temperature"])
                    humi = float(row["humidity"])
                except ValueError:
                    continue  # bỏ qua dòng lỗi

                if max_temp is None or temp > max_temp:
                    max_temp = temp
                if min_humi is None or humi < min_humi:
                    min_humi = humi

        return max_temp, min_humi

    except Exception as e:
        print("Lỗi đọc file CSV:", e)
        return None, None


def ThresholdAlert():
    temp_threshold, humi_threshold = threshold_from_database()
    max_temp, min_humi = read_extreme_from_log()

    if temp_threshold is None or humi_threshold is None:
        return False

    alert_temp = False
    alert_humi = False
    now = time.time()

    if max_temp is not None and max_temp > temp_threshold:
        alert_temp = True

    if min_humi is not None and min_humi < humi_threshold:
        alert_humi = True

    return alert_temp, alert_humi


