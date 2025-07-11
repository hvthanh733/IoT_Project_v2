import time
import board
import adafruit_dht
from gpiozero import DigitalInputDevice
import configparser
from Saver import SaveData

config = configparser.ConfigParser()
config.read("config.ini")

pin_dht = config.get("Block1", "GPIO1")
pin_fire = int(config.get("Block1", "GPIO2"))

dht_sensor = adafruit_dht.DHT11(getattr(board, pin_dht))
fire_sensor = DigitalInputDevice(pin_fire)

print("🔁 Bắt đầu đọc dữ liệu cảm biến... (Ctrl+C để dừng)")

while True:
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        fire = fire_sensor.value
        SaveData(temperature,humidity,fire, 1)
        print(f"Nhiệt độ: {temperature}°C")
        print(f"Độ ẩm: {humidity}%")
        print(f"Trạng thái lửa: {'Fire' if fire == 0 else 'No Fire'}")
    except Exception as e:
        print("Lỗi đọc cảm biến:", e)

    time.sleep(2)
