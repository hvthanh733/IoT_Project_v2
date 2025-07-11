import sqlite3
from services.password_hash import generate_password
from datetime import datetime, timedelta, date
conn = sqlite3.connect('iot_system.db')
cursor = conn.cursor()

# # -------------------------------
# # DROP tất cả các bảng (nếu có)
# # -------------------------------
# drop_tables = [
#     "DROP TABLE IF EXISTS sign_up_queue",
#     "DROP TABLE IF EXISTS fire_event",
#     "DROP TABLE IF EXISTS sensor_block_property",
#     "DROP TABLE IF EXISTS sensor_block_position",
#     "DROP TABLE IF EXISTS room",
#     "DROP TABLE IF EXISTS user"
# ]

# for sql in drop_tables:
#     cursor.execute(sql)

# print("[+] All tables dropped.")

# # -------------------------------
# # -------------------------------
# create_tables = [

#     '''
#     CREATE TABLE IF NOT EXISTS user (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL,
#         email TEXT,
#         phone TEXT,
#         role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user'))
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS room (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name_room TEXT UNIQUE,
#         size_m2 REAL,
#         x INTEGER,
#         y INTEGER,
#         z INTEGER
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS sensor_block_position (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_id INTEGER,
#         node INTEGER,
#         x REAL,
#         y REAL,
#         z REAL,
#         FOREIGN KEY (room_id) REFERENCES room(id)
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS sensor_block_property (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         block_id INTEGER,
#         date DATE,
#         sensor_type1 TEXT,
#         sensor_type2 TEXT,
#         threshold_temp_alert REAL,
#         threshold_humi_alert REAL,
#         max_temp REAL,
#         time_max_temp TEXT,
#         min_temp REAL,
#         time_min_temp TEXT,
#         max_humi REAL,
#         time_max_humi TEXT,
#         min_humi REAL,
#         time_min_humi TEXT,
#         FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
#     );

#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS fire_event (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_id INTEGER,
#         date TEXT NOT NULL,
#         time_start TEXT NOT NULL,
#         time_end TEXT,
#         note TEXT,
#         FOREIGN KEY (room_id) REFERENCES room(id)
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS sign_up_queue (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL,
#         email TEXT,
#         phone TEXT,
#         role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user')),
#         approved BOOLEAN DEFAULT 0
#     )
#     '''
# ]

# for sql in create_tables:
#     cursor.execute(sql)

# print("[+] All tables created.")

# # -------------------------------
# # -------------------------------
# admin_username = "admin"
# admin_password = "1"
# hashed_password = generate_password(admin_password)
# admin_email = "admin@example.com"
# admin_phone = "0123456789"

# try:
#     cursor.execute("""
#         INSERT INTO user (username, password, role)
#         VALUES (?, ?, 'admin')
#     """, (admin_username, hashed_password))
#     print("[+] Admin account created successfully.")
# except sqlite3.IntegrityError:
#     print("[!] Admin account already exists.")



# cursor.execute('''
#     INSERT INTO room (name_room, size_m2, x, y, z)
#     VALUES (?, ?, ?, ?, ?)
# ''', ('Machine Room', 60, 6, 5, 4))

# cursor.execute('''
#     INSERT INTO sensor_block_position (room_id, node, x, y, z)
#     VALUES (?, ?, ?, ?, ?)
# ''', (1, 1, 3, 2.5, 4))

# datelala = datetime.now().date()
# date_yesterday = datelala - timedelta(days=1)

# datelala = datetime.now().date()
# date_now = datelala + timedelta(days=1)
# cursor.execute('''
#     INSERT INTO sensor_block_property (
#         block_id,
#         date,
#         sensor_type1,
#         sensor_type2,
#         threshold_temp_alert,
#         threshold_humi_alert,
#         max_temp,
#         time_max_temp,
#         min_temp,
#         time_min_temp,
#         max_humi,
#         time_max_humi,
#         min_humi,
#         time_min_humi
#     )
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# ''', (
#     1,                      # block_id (id block vừa tạo)
#     date_yesterday,             # date
#     'DHT11',                # sensor_type1
#     'KY-026',                  # sensor_type2
#     None,                   # threshold_temp_alert = NULL
#     None,                   # threshold_humi_alert = NULL
#     36.5,                   # max_temp
#     '10:15:00',             # time_max_temp
#     24.2,                   # min_temp
#     '06:40:00',             # time_min_temp
#     70.1,                   # max_humi
#     '12:30:00',             # time_max_humi
#     50.3,                   # min_humi
#     '03:00:00'              # time_min_humi
# ))
# print("[+] Sample sensor_block_property record created with NULL thresholds.")
# # -------------------------------
# -------------------------------

conn.commit()
conn.close()
