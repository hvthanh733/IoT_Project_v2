import threading
import time
import configparser
import adafruit_dht
import board
from gpiozero import DigitalInputDevice
from Saver import saveData
from DataProcessing import read_and_aggregate_logs

# --- Cấu hình ---
config = configparser.ConfigParser()
config.read('config.ini')

# --- Số lượng Block ---
NUM_BLOCKS = 4

# --- Shared data ---
shared_datas = [{"temperature": None, "humidity": None, "fire_status": None} for _ in range(NUM_BLOCKS)]
data_locks = [threading.Lock() for _ in range(NUM_BLOCKS)]

# --- Lưu dữ liệu ---
def saveLoop(block_number, shared_data, data_lock):
    while True:
        with data_lock:
            t = shared_data["temperature"]
            h = shared_data["humidity"]
            f = shared_data["fire_status"]

        if t is not None and h is not None and f is not None:
            print(f"[block {block_number}] Saving: t={t}, h={h}, f={f}")
            saveData(t, h, f, block_number)
        else:
            print(f"[block {block_number}] Waiting for full data… t={t}, h={h}, f={f}")

        time.sleep(3)

# --- Đọc nhiệt độ và độ ẩm ---
def temperature_loop(block_index):
    block_name = f"Block{block_index + 1}"
    gpio_pin_str = config.get(block_name, "GPIO1")
    gpio_pin = getattr(board, gpio_pin_str)
    dht = adafruit_dht.DHT11(gpio_pin)

    print(f"[{block_name}][DHT11] Started on pin {gpio_pin_str}")
    while True:
        try:
            t = dht.temperature
            h = dht.humidity
            if t is not None and h is not None:
                print(f"[{block_name}][DHT11] {t:.1f}°C {h:.1f}%")
                with data_locks[block_index]:
                    shared_datas[block_index]["temperature"] = t
                    shared_datas[block_index]["humidity"] = h
            else:
                print(f"[{block_name}][DHT11] No data, retrying…")
        except RuntimeError as e:
            print(f"[{block_name}][DHT11] Error: {e}")
        time.sleep(2)

# --- Đọc trạng thái cảm biến lửa ---
def flame_loop(block_index):
    block_name = f"Block{block_index + 1}"
    pin = int(config.get(block_name, "GPIO2"))
    sensor = DigitalInputDevice(pin)

    print(f"[{block_name}][FlameSensor] Started on GPIO {pin}")
    while True:
        flame = sensor.value
        with data_locks[block_index]:
            shared_datas[block_index]["fire_status"] = 1 if flame == 0 else 0
        if flame == 0:
            print(f"[{block_name}] Flame detected!")
        time.sleep(2)

# --- Khởi tạo các thread cảm biến ---
def start_sensor_threads():
    for i in range(NUM_BLOCKS):
        threading.Thread(target=temperature_loop, args=(i,), daemon=True).start()
        threading.Thread(target=flame_loop, args=(i,), daemon=True).start()

# --- Khởi tạo các thread lưu dữ liệu ---
def start_save_threads():
    for i in range(NUM_BLOCKS):
        threading.Thread(target=saveLoop, args=(i + 1, shared_datas[i], data_locks[i]), daemon=True).start()

# --- Main ---
def main():
    start_sensor_threads()
    print("[main] Sensor threads started. Starting save threads…")
    start_save_threads()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    main()
