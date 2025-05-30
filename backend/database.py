import sqlite3
from utils import pass_controller
# Kết nối đến database (sẽ tạo mới nếu chưa có)
conn = sqlite3.connect("iot_system.db")
cursor = conn.cursor()

# Tạo bảng room
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS room (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name_room   TEXT UNIQUE,
#     size_m2     REAL
# )
# """)

# # Tạo bảng sensor_block_position
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sensor_block_position (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     room_id         INTEGER,
#     x               INTEGER,
#     y               INTEGER,
#     FOREIGN KEY (room_id) REFERENCES room(id)
# )
# """)

# # Tạo bảng sensor_block_property
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sensor_block_property (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     block_name          TEXT,
#     sensor_type1        TEXT,
#     coverage_sensor1    REAL,
#     sensor_type2        TEXT,
#     coverage_sensor2    REAL,
#     threshold_temp_max  REAL,
#     threshold_temp_min  REAL,
#     threshold_humi_max  REAL,
#     threshold_humi_min  REAL,
#     fire_state_alert    BOOLEAN,
#     FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
# )
# """)

# # Tạo bảng sensor_block_data
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS sensor_block_data (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     date                DATETIME,
#     block_id            INTEGER,
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

# # Tạo bảng user
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
# Tạo bảng user
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
# Danh sách các bảng cần reset ID
table = [
    # "room",
    # "sensor_block_position",
    # "sensor_block_property",
    # "sensor_block_data",
    "user"
]



# Xóa toàn bộ dữ liệu trong bảng user
# cursor.execute("DELETE FROM user;")

# cursor.execute("DELETE FROM sqlite_sequence WHERE name='user';")

#  Thiet lap user
users = [
    ("admin", "1", None, None, "admin"),
    ("thanh", pass_controller.hash_password("1"), "thanh@gmail.com", "0123456789", "user")
    # ("nam", "1", "nam@mail.com", "0901234567", "user"),
    # ("mai", "1", "mai@mail.com", "0934567890", "user")
]
# x = pass_controller.hash_password("1")
# kq = pass_controller.verify_password("1", x)
# if kq == True:
#     print("oke r")
# else:
#     print("sai r")


for u in users:
    try:
        cursor.execute("""
        INSERT INTO user (username, password, email, phone, role)
        VALUES (?, ?, ?, ?, ?)
        """, u)
    except sqlite3.IntegrityError:
        print(f"Tài khoản '{u[0]}' đã tồn tại.")


# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Tạo bảng thành công.")
