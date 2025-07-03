import csv
import os
from datetime import datetime
import sqlite3

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


# --- Create File CSV ---
def makeFile():
    today = datetime.now().strftime("%Y%m%d")
    folder_path = os.path.join("logs", today)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "block1_data.csv")

    try:
        if not os.path.exists(file_path):
            # If file not exist, create new
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
        else:
            # Check max line, if > MAX_LINES delete file and create new
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            if lines >= MAX_LINES:
                os.remove(file_path)
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["time_stemp", "temperature", "humidity", "fire_state"])
    except Exception as e:
        print(f"Error: {e}")

    return file_path

last_data = {"temperature": None, "humidity": None, "fire_state": None}

def saveDataFromSTM32(temperature, humidity, fire_state):
    file_path = makeFile()
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    temp = float(row["temperature"])
                    humi = float(row["humidity"])
                except ValueError:
                    continue
                if temp == temperature and humi == humidity:
                    return

    time_stamp = datetime.now().strftime("%H:%M:%S")
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time_stamp, temperature, humidity, fire_state])

def delete_csv_file():
    today = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join("logs", today, "block1_data.csv")

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error when delete file: {e}")
    else:
        print(f"File not exist: {file_path}")

def read_CSV():
    today = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join("logs", today, "block1_data.csv")
    if not os.path.exists(file_path):
        return None

    max_temp = float('-inf')
    min_temp = float('inf')
    max_temp_time = min_temp_time = ""

    max_humi = float('-inf')
    min_humi = float('inf')
    max_humi_time = min_humi_time = ""

    fire_transitions = []
    prev_fire_state = None

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp = float(row['temperature'])
            humi = float(row['humidity'])
            time = row['time_stemp']
            fire_state = float(row['fire_state'])

            # Temperature
            if temp > max_temp:
                max_temp = temp
                max_temp_time = time
            if temp < min_temp:
                min_temp = temp
                min_temp_time = time

            # Humidity
            if humi > max_humi:
                max_humi = humi
                max_humi_time = time
            if humi < min_humi:
                min_humi = humi
                min_humi_time = time

            # # Save if fire_state changed
            if prev_fire_state is None or fire_state != prev_fire_state:
                fire_transitions.append({
                    "time_stemp": time,
                    "temperature": temp,
                    "humidity": humi,
                    "fire_state": fire_state
                })

            prev_fire_state = fire_state
    return {
        "time_stemp": time,
        "temperature": {
            "max": (max_temp, max_temp_time),
            "min": (min_temp, min_temp_time),
        },
        "humidity": {
            "max": (max_humi, max_humi_time),
            "min": (min_humi, min_humi_time),
        },
        "fire_changes": fire_transitions
    }
