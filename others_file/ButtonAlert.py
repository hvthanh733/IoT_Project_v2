from gpiozero import Button
import configparser
import time
from datetime import datetime
import pause
button1 = Button(19, pull_up=True)


def ButtonAlert():
    print("hello")

button1.when_pressed = ButtonAlert
pause()
# from gpiozero import Button
# from signal import pause
# import time
# from Saver import save_event

# from datetime import datetime
# from LedAlert import blink_led
# import configparser

# config = configparser.ConfigParser()
# config.read("config.ini")
# gpio_pin = int(config["Button1"]["GPIO"])
# button1 = Button(gpio_pin, pull_up=True, bounce_time=0.2)

# last_press_time = 0
# min_interval = 2.0  # giây giữa 2 lần nhấn
# is_processing = False  


# def ButtonAlert():
#     global last_press_time, is_processing
#     now = time.time()

#     if is_processing:
#         print("Đang xử lý... bỏ qua lần nhấn này.")
#         return

#     if now - last_press_time >= min_interval:
#         is_processing = True
#         node = "Human click"
#         save_event(node)
#         # blink_led()  # mất khoảng 5 giây để nhấp nháy
#         last_press_time = time.time()
#         is_processing = False


# print("Đang chờ nhấn nút GPIO 19...")

# init_db()
# button.when_activated = ButtonAlert

