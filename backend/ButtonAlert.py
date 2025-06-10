from gpiozero import Button
from signal import pause
import time
import sqlite3
from datetime import datetime

button = Button(19, pull_up=True, bounce_time=0.2)

last_press_time = 0
min_interval = 2.0  # giây giữa 2 lần nhấn

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

def save_button_event(note="Ghi chú mặc định"):
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

    print(f"Đã lưu nút bấm lúc {date} {time_start}")

def on_press():
    global last_press_time
    now = time.time()
    if now - last_press_time >= min_interval:
        save_button_event()
        last_press_time = now

print("🟢 Đang chờ nhấn nút GPIO 19...")

init_db()
button.when_activated = on_press

pause()
