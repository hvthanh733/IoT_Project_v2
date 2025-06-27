import sqlite3
from services.password_hash import generate_password, verify_pass

# Kết nối đến database (sẽ tạo mới nếu chưa có)
conn = sqlite3.connect("iot_system.db")
cursor = conn.cursor()

# cursor.execute("DROP TABLE IF EXISTS room")


# # cursor.execute("""
# # INSERT OR IGNORE INTO room (name_room, size_m2, x, y, z)
# # VALUES (?, ?, ?, ?, ?)
# # """, ("machine room", 20.0, 4, 5, 3))

# # Tạo bảng sensor_block_position
# # cursor.execute("DROP TABLE IF EXISTS sensor_block_position")


# cursor.execute("""
# CREATE TABLE IF NOT EXISTS room (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name_room   TEXT UNIQUE,
#     size_m2     REAL,
#     x           INTEGER,
#     y           INTEGER,
#     z           INTEGER
# )
# """)


# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sensor_block_position (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     room_id INTEGER,
#     node    TEXT,
#     x       REAL,
#     y       REAL,
#     z       REAL,
#     FOREIGN KEY (room_id) REFERENCES room(id)
# )
# """)


# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sensor_block_property (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     block_id                INTEGER UNIQUE,
#     sensor_type1            TEXT,
#     sensor_type2            TEXT,
#     threshold_temp_alert    REAL,
#     threshold_humi_alert    REAL,
#     max_temp            REAL,
#     min_temp            REAL,
#     time_max_temp       TIME,
#     time_min_temp       TIME,
#     max_humi            REAL,
#     min_humi            REAL,
#     time_max_humi       TIME,
#     time_min_humi       TIME,
#     fire_state          BOOLEAN,
#     fire_state_human    BOOLEAN,
#     start_time          TIME,
#     end_time            TIME,
#     FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
# )
# """)

# # Tạo bảng mới
# cursor.execute("""
#     CREATE TABLE fire_event (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_id INTEGER,
#         date TEXT NOT NULL,
#         time_start TEXT NOT NULL,
#         time_end TEXT,
#         note TEXT
#     );
# """)
# # cursor.execute("""
# # CREATE TABLE IF NOT EXISTS user (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     username TEXT UNIQUE NOT NULL,
# #     password TEXT NOT NULL,
# #     email TEXT,
# #     phone TEXT,
# #     role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user'
# # )
# # """)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sign_up_queue (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     email TEXT,
#     phone TEXT,
#     role TEXT DEFAULT 'user',   -- Chú ý: phải là kiểu TEXT, không phải 'role user'
#     approved BOOLEAN DEFAULT 0  -- 0: chưa duyệt, 1: đã duyệt
# );

# """)


# # cursor.execute("""
# # UPDATE sensor_block_property
# # SET threshold_temp_alert = ?, threshold_humi_alert = ?
# # WHERE block_id = ?
# # """, (60.0, 40.0, 1))

# # # Tạo bảng user
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS user (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     email TEXT,
#     phone TEXT,
#     role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user'
# )
# """)




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

# # Tạo bảng user

# # Danh sách các bảng cần reset ID
# tables = [
#     "user",
#     "sign_up_queue"
# ]

# # for table in tables:
# #     cursor.execute(f"DELETE FROM {table};")  # Xoá dữ liệu
# #     cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")  # Reset AUTOINCREMENT (nếu có)

# # #  Thiet lap user
# users = [
#     ("admin", generate_password("1"), None, None, "admin"),
#     ("kien", generate_password("1"), "kien@gmail.com", "0123456789", "user")
#     # ("nam", "1", "nam@mail.com", "0901234567", "user"),
#     # ("mai", "1", "mai@mail.com", "0934567890", "user")
# ]
# # verify_pass("1",generate_password("1"))
# # print(verify_pass("1",generate_password("1")))
# # print(generate_password("1"))
# # x = pass_controller.hash_password("1")
# # kq = pass_controller.verify_password("1", x)
# # if kq == True:
# #     print("oke r")
# # else:
# #     print("sai r")


# # for u in users:
# #     try:
# #         cursor.execute("""
# #         INSERT INTO user (username, password, email, phone, role)
# #         VALUES (?, ?, ?, ?, ?)
# #         """, u)
# #     except sqlite3.IntegrityError:
# #         print(f"Tài khoản '{u[0]}' đã tồn tại.")

# # from datetime import datetime, timedelta
# # cursor.execute("DROP TABLE IF EXISTS button_alert;")  # XÓA bảng cũ

# # Xóa bảng cũ
# # cursor.execute("DROP TABLE button_alert;")

# # # Tạo bảng mới
# # cursor.execute("""
# #     CREATE TABLE fire_event (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         room_id INTEGER,
# #         date TEXT NOT NULL,
# #         time_start TEXT NOT NULL,
# #         time_end TEXT,
# #         note TEXT
# #     );
# # """)



# # Thiết lập thông tin
# base_date = "2025-01-09"
# start_time = datetime.strptime("09:00:00", "%H:%M:%S")

# # Tạo 10 bản ghi
# for i in range(10):
#     time_start_str = (start_time + timedelta(hours=i)).strftime("%H:%M:%S")
#     cursor.execute("""
#         INSERT INTO button_alert (date, time_start, time_end, note)
#         VALUES (?, ?, NULL, ?)
#     """, (base_date, time_start_str, "Hello"))

# cursor.execute("DELETE FROM button_alert")
# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Tạo bảng thành công.")
