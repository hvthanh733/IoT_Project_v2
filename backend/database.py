import sqlite3

# Kết nối đến database (sẽ tạo mới nếu chưa có)
conn = sqlite3.connect("iot_system.db")
cursor = conn.cursor()

# Tạo bảng room
cursor.execute("""
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_room   TEXT UNIQUE,
    size_m2     REAL
)
""")

# Tạo bảng sensor_block_position
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_block_position (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id         INTEGER,
    x               INTEGER,
    y               INTEGER,
    FOREIGN KEY (room_id) REFERENCES room(id)
)
""")

# Tạo bảng sensor_block_property
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_block_property (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id            INTEGER,
    block_name          TEXT,
    sensor_type1        TEXT,
    coverage_sensor1    REAL,
    sensor_type2        TEXT,
    coverage_sensor2    REAL,
    threshold_temp_max  REAL,
    threshold_temp_min  REAL,
    threshold_humi_max  REAL,
    threshold_humi_min  REAL,
    FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
)
""")

# Tạo bảng sensor_block_data
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_block_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date                DATETIME,
    block_id            INTEGER,
    max_temp            REAL,
    min_temp            REAL,
    time_max_temp       TIME,
    time_min_temp       TIME,
    max_humi            REAL,
    min_humi            REAL,
    time_max_humi       TIME,
    time_min_humi       TIME,
    fire_state          BOOLEAN,
    fire_state_human    BOOLEAN,
    start_time          TIME,
    end_time            TIME,
    FOREIGN KEY (block_id) REFERENCES sensor_block_position(id)
)
""")


# Danh sách các bảng cần reset ID
tables = [
    "room",
    "sensor_block_position",
    "sensor_block_property",
    "sensor_block_data"
]

# Xóa dữ liệu và reset AUTOINCREMENT cho từng bảng
for table in tables:
    cursor.execute(f"DELETE FROM {table};")  # Xóa toàn bộ dữ liệu
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")  # Reset ID

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Tạo bảng thành công.")
