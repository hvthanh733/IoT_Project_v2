from gpiozero import LED
import configparser
import time

config = configparser.ConfigParser()
config.read("config.ini")
led_pin = int(config["Led"]["GPIO"])

led = 22  # định nghĩa led 1 lần, dùng cho cả 2 hàm

def blink_led():
    print("LED nhấp nháy...")
    for i in range(5):
        print(f"Nhấp nháy lần {i+1}")
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
    return True
