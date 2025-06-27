import sqlite3
from services.password_hash import generate_password, verify_pass

conn = sqlite3.connect('iot_system.db')
cursor = conn.cursor()

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
#         z INTEGER,
#         user_id INTEGER,
#         FOREIGN KEY (user_id) REFERENCES user(id)
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS sensor_block_position (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_id INTEGER,
#         node TEXT,
#         x REAL,
#         y REAL,
#         z REAL,
#         FOREIGN KEY (room_id) REFERENCES room(id)
#     )
#     ''',

#     '''
#     CREATE TABLE IF NOT EXISTS sensor_block_property (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         block_id INTEGER UNIQUE,
#         sensor_type1 TEXT,
#         sensor_type2 TEXT,
#         threshold_temp_alert REAL,
#         threshold_humi_alert REAL,
#         max_temp REAL,
#         min_temp REAL,
#         time_max_temp TEXT,
#         time_min_temp TEXT,
#         max_humi REAL,
#         min_humi REAL,
#         time_max_humi TEXT,
#         time_min_humi TEXT,
#         fire_state BOOLEAN,
#         fire_state_human BOOLEAN,
#         start_time TEXT,
#         end_time TEXT,
#         FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
#     )
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


admin_username = "admin"
admin_password = "1"
hashed_password = generate_password(admin_password)
admin_email = "admin@example.com"
admin_phone = "0123456789"

try:
    cursor.execute("""
        INSERT INTO user (username, password, email, phone, role)
        VALUES (?, ?, ?, ?, 'admin')
    """, (admin_username, hashed_password, admin_email, admin_phone))
    print("[+] Admin account created successfully.")
except sqlite3.IntegrityError:
    print("[!] Admin account already exists.")


conn.commit()
conn.close()
