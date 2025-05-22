import sqlite3

# Kết nối đến database (sẽ tạo mới nếu chưa có)
conn = sqlite3.connect("iot_system.db")
cursor = conn.cursor()

# Tạo bảng sensor_block
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS sensor_block (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     room_id INTEGER,
#     x INTEGER,
#     y INTEGER,
#     description TEXT
# )
# ''')

# Tạo bảng sensor
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER,
    type TEXT,
    coverage_radius INTEGER,
    FOREIGN KEY (block_id) REFERENCES sensor_block(id)
)
''')

# Tạo bảng sensor_data
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id       INTEGER,
    max_temp       REAL,
    min_temp       REAL,
    time_max_temp  DATETIME,
    time_min_temp  DATETIME,
    do_am          REAL,
    do_am_max      REAL,
    do_am_min      REAL,
    time_max_humi  DATETIME,
    time_min_humi  DATETIME,
    fire_state     BOOLEAN,
    time_start     DATETIME,
    total_time     REAL,
    FOREIGN KEY (block_id) REFERENCES sensor_block(id)
)
''')


# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("✅ Tạo bảng thành công.")
