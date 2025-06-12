from ThresholdAlert import ThresholdAlert
from Saver import SaveData, init_db, save_event
from gpiozero import Button as GPIOButton
from gpiozero import DigitalInputDevice, LED
from signal import pause
import board, adafruit_dht, configparser, threading, time

# Đọc cấu hình
config = configparser.ConfigParser()
config.read("config.ini")
gpio_pin1 = int(config["Button1"]["GPIO"])  # Nút khẩn cấp
gpio_pin2 = int(config["Button2"]["GPIO"])  # Nút kết thúc
led_pin = int(config["Led"]["GPIO"])

# Khởi tạo thiết bị
human_click = GPIOButton(gpio_pin1, pull_up=True, bounce_time=0.2)
end_event = GPIOButton(gpio_pin2, pull_up=True, bounce_time=0.2)
led = LED(led_pin)

# Trạng thái hệ thống
alarm_active = False

# Hàm nhấn nút khẩn cấp
def on_human_click_pressed():
    global alarm_active
    if not alarm_active:
        save_event("Khẩn cấp: Người dùng bấm nút khẩn cấp!")
        print("[ALERT] Kích hoạt cảnh báo khẩn cấp!")
        alarm_active = True

# Hàm nhấn nút kết thúc
def on_end_event_pressed():
    global alarm_active
    if alarm_active:
        save_event("Đã kết thúc báo động do người dùng nhấn nút END")
        print("[INFO] Tắt cảnh báo.")
        alarm_active = False

# Nháy LED khi cảnh báo hoạt động
def blink_led_loop():
    global alarm_active
    while True:
        if alarm_active:
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
        else:
            led.off()
            time.sleep(0.1)

# Gán sự kiện nhấn nút
human_click.when_pressed = on_human_click_pressed
end_event.when_pressed = on_end_event_pressed

# Loop đọc cảm biến (để trống nếu chưa dùng)
def sensor_loop():
    config = configparser.ConfigParser()
    config.read("config.ini")
    pin_dht = config.get("Block1", "GPIO1")
    pin_fire = int(config.get("Block1", "GPIO2"))
    dht_sensor = adafruit_dht.DHT11(getattr(board, pin_dht))
    fire_sensor = DigitalInputDevice(pin_fire)
    print(f"[INIT] DHT: {pin_dht} | Fire: {pin_fire}")

    while True:
        try:
            temp = dht_sensor.temperature
            humi = dht_sensor.humidity
            fire = fire_sensor.value
            SaveData(temp, humi, fire)
        except Exception as e:
            print("Sensor error:", e)
        time.sleep(2)
    pass

# Loop cảnh báo theo cảm biến
def alert_loop():
    global alarm_active
    while True:
        alert_temp, alert_humi = ThresholdAlert()
        if (alert_temp or alert_humi) and not alarm_active:
            msg = "Nguy hiểm:"
            if alert_temp: msg += " Nhiệt độ vượt ngưỡng!"
            if alert_humi: msg += " Độ ẩm vượt ngưỡng!"
            save_event(msg)
            print("[ALERT]", msg)
            alarm_active = True

        time.sleep(0.5)

# Khởi động hệ thống
if __name__ == "__main__":
    print("Khởi động hệ thống...")
    init_db()

    thread_sensor = threading.Thread(target=sensor_loop)
    thread_alert = threading.Thread(target=alert_loop)
    thread_blink = threading.Thread(target=blink_led_loop)

    thread_sensor.start()
    thread_alert.start()
    thread_blink.start()

    pause()
