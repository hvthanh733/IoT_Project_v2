import time
import board
import adafruit_dht
from gpiozero import DigitalInputDevice
import configparser
import threading
from Saver import saveData 
config = configparser.ConfigParser()
config.read("config.ini")

sensor_data_all12 = {}
sensor_data_all34 = {}

data_lock12 = threading.Lock()
data_lock34 = threading.Lock()

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

def read_block(block_name, data_dict, lock):
    dht_sensor, fire_sensor = get_sensor_instances(block_name)
    if dht_sensor is None or fire_sensor is None:
        return

    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        fire = fire_sensor.value
    except Exception as e:
        temperature = None
        humidity = None
        fire = None
        print(f"[{block_name}] Lỗi đọc cảm biến: {e}")

    with lock:
        data_dict[block_name] = {
            "temperature": temperature,
            "humidity": humidity,
            "fire": "Fire" if fire == 0 else "No Fire"
        }
    time.sleep(1)
    
def value_all_blocks12():
    global sensor_data_all12
    sensor_data_all12 = {}
    block_names = ["Block1", "Block2"]
    threads = []

    for name in block_names:
        t = threading.Thread(target=read_block, args=(name, sensor_data_all12, data_lock12))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for block_name, data in sensor_data_all12.items():
        block_number = int(block_name[-1]) 
        saveData(
            temperature=data["temperature"],
            humidity=data["humidity"],
            fire_status=data["fire"],
            block_number=block_number
        )
    return sensor_data_all12

# # Đọc Block3 và Block4
# def value_all_blocks34():
#     global sensor_data_all34
#     sensor_data_all34 = {}
#     block_names = ["Block3", "Block4"]
#     threads = []

#     for name in block_names:
#         t = threading.Thread(target=read_block, args=(name, sensor_data_all34, data_lock34))
#         t.start()
#         threads.append(t)

#     for t in threads:
#         t.join()
#     for block_name, data in sensor_data_all34.items():
#         block_number = int(block_name[-1])  # Từ "Block3" → số 3
#         saveData(
#             temperature=data["temperature"],
#             humidity=data["humidity"],
#             fire_status=data["fire"],
#             block_number=block_number
#         )
#     return sensor_data_all34
