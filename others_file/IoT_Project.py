import threading
import time
import configparser
import adafruit_dht
import board
from gpiozero import DigitalInputDevice
from Saver import saveData
from DataProcessing import readLog

# --- Cấu hình ---
config = configparser.ConfigParser()
config.read('config.ini')

# --- Số lượng Block ---
# NUM_BLOCKS = 4

# # --- Shared data ---
# shared_datas = [{"temperature": None, "humidity": None, "fire_status": None} for _ in range(NUM_BLOCKS)]
# data_locks = [threading.Lock() for _ in range(NUM_BLOCKS)]

# # --- Lưu dữ liệu ---
# def saveLoop(block_number, shared_data, data_lock):
#     while True:
#         with data_lock:
#             t = shared_data["temperature"]
#             h = shared_data["humidity"]
#             f = shared_data["fire_status"]

#         if t is not None and h is not None and f is not None:
#             print(f"[block {block_number}] Saving: t={t}, h={h}, f={f}")
#             saveData(t, h, f, block_number)
#         else:
#             print(f"[block {block_number}] Waiting for full data… t={t}, h={h}, f={f}")

#         time.sleep(5)

# # --- Đọc nhiệt độ và độ ẩm ---
# def temperature_loop(block_index):
#     block_name = f"Block{block_index + 1}"
#     gpio_pin_str = config.get(block_name, "GPIO1")
#     gpio_pin = getattr(board, gpio_pin_str)
#     dht = adafruit_dht.DHT11(gpio_pin)

#     print(f"[{block_name}][DHT11] Started on pin {gpio_pin_str}")
#     while True:
#         try:
#             t = dht.temperature
#             h = dht.humidity
#             if t is not None and h is not None:
#                 print(f"[{block_name}][DHT11] {t:.1f}°C {h:.1f}%")
#                 with data_locks[block_index]:
#                     shared_datas[block_index]["temperature"] = t
#                     shared_datas[block_index]["humidity"] = h
#             else:
#                 print(f"[{block_name}][DHT11] No data, retrying…")
#         except RuntimeError as e:
#             print(f"[{block_name}][DHT11] Error: {e}")
#         time.sleep(5)

# # --- Đọc trạng thái cảm biến lửa ---
# def flame_loop(block_index):
#     block_name = f"Block{block_index + 1}"
#     pin = int(config.get(block_name, "GPIO2"))
#     sensor = DigitalInputDevice(pin)

#     print(f"[{block_name}][FlameSensor] Started on GPIO {pin}")
#     while True:
#         flame = sensor.value
#         with data_locks[block_index]:
#             shared_datas[block_index]["fire_status"] = 1 if flame == 0 else 0
#         if flame == 0:
#             print(f"[{block_name}] Flame detected!")
#         time.sleep(5)

# # --- Khởi tạo các thread cảm biến ---
# def start_sensor_threads():
#     for i in range(NUM_BLOCKS):
#         threading.Thread(target=temperature_loop, args=(i,), daemon=True).start()
#         threading.Thread(target=flame_loop, args=(i,), daemon=True).start()

# # --- Khởi tạo các thread lưu dữ liệu ---
# def start_save_threads():
#     for i in range(NUM_BLOCKS):
#         threading.Thread(target=saveLoop, args=(i + 1, shared_datas[i], data_locks[i]), daemon=True).start()

# def readLogThread():
#     while True:
#         readLog()
#         time.sleep(7)
# --- Main ---
# def main():

#     print("[main] Sensor threads started. Starting save threads…")
#     start_sensor_threads()
#     start_save_threads()
#     threading.Thread(target=readLogThread, daemon=True).start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Stopping...")

# if __name__ == "__main__":
#     main()
#     while True:
#         time.sleep(1)



def DHT11_value():
    block_name = "Block1"
    pin1 = config.get(block_name, "GPIO1")  # Ví dụ: 'D20'
    gpio_pin1 = adafruit_dht.DHT11(getattr(board, pin1))

    pin2 = int(config.get(block_name, "GPIO2"))  # Ví dụ: 21
    gpio_pin2 = DigitalInputDevice(pin2)

    try:
        time.sleep(2)  # Chờ cảm biến ổn định
        temperature = gpio_pin1.temperature
        humidity = gpio_pin1.humidity
    except RuntimeError as e:
        print(f"Lỗi đọc DHT11: {e}")
        temperature = None
        humidity = None
    finally:
        gpio_pin1.exit()  # Giải phóng tài nguyên

    return temperature, humidity, gpio_pin2.value, pin2  # thêm cả số GPIO để in

def readValue(temperature, humidity, fire_status, fire_pin):
    print(f"Nhiệt độ: {temperature}°C, Độ ẩm: {humidity}%")
    if fire_status == 0:
        print(f"Có lửa (GPIO{fire_pin})")
    else:
        print(f"Không có lửa (GPIO{fire_pin})")

def main():
    while True:
        temperature, humidity, fire_status, fire_pin = DHT11_value()
        readValue(temperature, humidity, fire_status, fire_pin)
        time.sleep(2)  # tránh đọc quá nhanh

if __name__ == "__main__":
    main()







import time
import board
import adafruit_dht
from gpiozero import DigitalInputDevice
import configparser
import threading

config = configparser.ConfigParser()
config.read("config.ini")

sensor_data_all = {}
data_lock = threading.Lock()

# Chỉ khởi tạo 1 lần cảm biến
sensor_instances = {}

def get_sensor_instances(block_name):
    if block_name in sensor_instances:
        return sensor_instances[block_name]

    try:
        pin1 = config.get(block_name, "GPIO1")
        dht_sensor = adafruit_dht.DHT11(getattr(board, pin1))

        pin2 = int(config.get(block_name, "GPIO2"))
        fire_sensor = DigitalInputDevice(pin2)

        sensor_instances[block_name] = (dht_sensor, fire_sensor)
        return dht_sensor, fire_sensor
    except Exception as e:
        print(f"[{block_name}] Lỗi khi khởi tạo cảm biến: {e}")
        return None, None

def read_block(block_name):
    dht_sensor, fire_sensor = get_sensor_instances(block_name)
    if dht_sensor is None or fire_sensor is None:
        return

    try:
        time.sleep(1)

        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        fire = fire_sensor.value

    except Exception as e:
        temperature = None
        humidity = None
        fire = None
        print(f"[{block_name}] Lỗi đọc cảm biến: {e}")

    with data_lock:
        sensor_data_all[block_name] = {
            "temperature": temperature,
            "humidity": humidity,
            "fire": "🔥 Có lửa" if fire == 0 else "✅ Không có lửa"
        }

def value_all_blocks():
    global sensor_data_all
    sensor_data_all = {}

    block_names = ["Block1", "Block2"]
    threads = []

    for name in block_names:
        t = threading.Thread(target=read_block, args=(name,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return sensor_data_all 