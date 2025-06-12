from gpiozero import LED
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
led_pin = int(config["Led"]["GPIO"])

def blink_led(pin=led_pin):
    led = LED(pin)
    for i in range(5):
        print(f"Nhấp nháy lần {i+1}")
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
    led.off()

