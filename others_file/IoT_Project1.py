import threading
import time
import configparser
import adafruit_dht
import board
from gpiozero import DigitalInputDevice
from Saver import saveData

# --- Cấu hình ---
config = configparser.ConfigParser()
config.read('config.ini')

# --- Shared ---

shared_data1 = {"temperature": None, "humidity": None, "fire_status": None}
shared_data2 = {"temperature": None, "humidity": None, "fire_status": None}
shared_data3 = {"temperature": None, "humidity": None, "fire_status": None}
shared_data4 = {"temperature": None, "humidity": None, "fire_status": None}
data_lock1 = threading.Lock()
data_lock2 = threading.Lock()
data_lock3 = threading.Lock()
data_lock4 = threading.Lock()

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


# --- Thread DHT11 ---
def Temperature1():
    gpio_pin_str = config.get("Block1", "GPIO1")
    gpio_pin = getattr(board, gpio_pin_str)

    dht = adafruit_dht.DHT11(gpio_pin)
    print(f"[Temperature1] Started on pin {gpio_pin_str}")
    while True:
        try:
            t = dht.temperature
            h = dht.humidity
            if t is not None and h is not None:
                print(f"[Block1][DHT11] {t:.1f}°C {h:.1f}%")
                with data_lock1:
                    shared_data1["temperature"], shared_data1["humidity"] = t, h
            else:
                print("[Block1][DHT11] No data, retrying…")
        except RuntimeError as e:
            print(f"[Block1][DHT11] Error: {e}")
        time.sleep(2)

# --- Thread FlameSensor ---
def FlameSensor1():
    pin = int(config.get("Block1", "GPIO2"))
    sensor = DigitalInputDevice(pin)
    print(f"[Block1][FlameSensor1] Started on GPIO {pin}")
    while True:
        flame = sensor.value  # 0 or 1
        with data_lock1:
            shared_data1["fire_status"] = 1 if flame == 0 else 0
        if flame == 0:
            print("[Block1] Flame detected!")
        time.sleep(2)

###########
# --- Thread DHT11 ---
def Temperature2():
    gpio_pin_str = config.get("Block2", "GPIO1")
    gpio_pin = getattr(board, gpio_pin_str)

    dht = adafruit_dht.DHT11(gpio_pin)
    print(f"[Temperature2] Started on pin {gpio_pin_str}")
    while True:
        try:
            t = dht.temperature
            h = dht.humidity
            if t is not None and h is not None:
                print(f"[Block2][DHT11] {t:.1f}°C {h:.1f}%")
                with data_lock2:
                    shared_data2["temperature"], shared_data2["humidity"] = t, h
            else:
                print("[Block2][DHT11] No data, retrying…")
        except RuntimeError as e:
            print(f"[Block2][DHT11] Error: {e}")
        time.sleep(2)

# --- Thread FlameSensor ---
def FlameSensor2():
    pin = int(config.get("Block2", "GPIO2"))
    sensor = DigitalInputDevice(pin)
    print(f"[Block2][FlameSensor2] Started on GPIO {pin}")
    while True:
        flame = sensor.value  # 0 or 1
        with data_lock2:
            shared_data2["fire_status"] = 1 if flame == 0 else 0
        if flame == 0:
            print("[Block2] Flame detected!")
        time.sleep(2)

###########
# --- Thread DHT11 ---
def Temperature3():
    gpio_pin_str = config.get("Block3", "GPIO1")
    gpio_pin = getattr(board, gpio_pin_str)

    dht = adafruit_dht.DHT11(gpio_pin)
    print(f"[Temperature3] Started on pin {gpio_pin_str}")
    while True:
        try:
            t = dht.temperature
            h = dht.humidity
            if t is not None and h is not None:
                print(f"[Block3][DHT11] {t:.1f}°C {h:.1f}%")
                with data_lock3:
                    shared_data3["temperature"], shared_data3["humidity"] = t, h
            else:
                print("[Block3][DHT11] No data, retrying…")
        except RuntimeError as e:
            print(f"[Block3][DHT11] Error: {e}")
        time.sleep(2)

# --- Thread FlameSensor ---
def FlameSensor3():
    pin = int(config.get("Block3", "GPIO2"))
    sensor = DigitalInputDevice(pin)
    print(f"[Block3][FlameSensor3] Started on GPIO {pin}")
    while True:
        flame = sensor.value  # 0 or 1
        with data_lock3:
            shared_data3["fire_status"] = 1 if flame == 0 else 0
        if flame == 0:
            print("[Block3] Flame detected!")
        time.sleep(2)

###########
# --- Thread DHT11 ---
def Temperature4():
    gpio_pin_str = config.get("Block4", "GPIO1")
    gpio_pin = getattr(board, gpio_pin_str)

    dht = adafruit_dht.DHT11(gpio_pin)
    print(f"[Temperature4] Started on pin {gpio_pin_str}")
    while True:
        try:
            t = dht.temperature
            h = dht.humidity
            if t is not None and h is not None:
                print(f"[Block4][DHT11] {t:.1f}°C {h:.1f}%")
                with data_lock4:
                    shared_data4["temperature"], shared_data4["humidity"] = t, h
            else:
                print("[Block4][DHT11] No data, retrying…")
        except RuntimeError as e:
            print(f"[Block4][DHT11] Error: {e}")
        time.sleep(2)

# --- Thread FlameSensor ---
def FlameSensor4():
    pin = int(config.get("Block4", "GPIO2"))
    sensor = DigitalInputDevice(pin)
    print(f"[Block4][FlameSensor4] Started on GPIO {pin}")
    while True:
        flame = sensor.value  # 0 or 1
        with data_lock4:
            shared_data4["fire_status"] = 1 if flame == 0 else 0
        if flame == 0:
            print("[Block4] Flame detected!")
        time.sleep(2)

# --- Khởi thread ---
def block1():
    threading.Thread(target=Temperature1, daemon=True).start()
    threading.Thread(target=FlameSensor1, daemon=True).start()

def block2():
    threading.Thread(target=Temperature2, daemon=True).start()
    threading.Thread(target=FlameSensor2, daemon=True).start()

def block3():
    threading.Thread(target=Temperature3, daemon=True).start()
    threading.Thread(target=FlameSensor3, daemon=True).start()

def block4():
    threading.Thread(target=Temperature4, daemon=True).start()
    threading.Thread(target=FlameSensor4, daemon=True).start()


# --- Main ---
def main():
    block1()
    block2() 
    block3()
    block4() 
    print("[main] Sensor threads started. Starting save threads…")

    # 4 thread 
    threading.Thread(target=saveLoop, args=(1, shared_data1, data_lock1), daemon=True).start()
    threading.Thread(target=saveLoop, args=(2, shared_data2, data_lock2), daemon=True).start()
    threading.Thread(target=saveLoop, args=(3, shared_data3, data_lock3), daemon=True).start()
    threading.Thread(target=saveLoop, args=(4, shared_data4, data_lock4), daemon=True).start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stop processing.")

if __name__ == "__main__":
    main()
