# import serial
# import time

# ser = serial.Serial(
#     port='/dev/ttyAMA0',
#     baudrate=115200,
#     timeout=1
# )

# print("Đang lắng nghe dữ liệu dạng HEX từ STM32...")

# while True:
#     if ser.in_waiting > 0:
#         data = ser.read(ser.in_waiting)  # đọc tất cả bytes có sẵn
#         hex_string = ' '.join(f'{b:02X}' for b in data)
#         print("Nhận được (hex):", hex_string)
#     time.sleep(0.1)

import serial
import time

print("Đang lắng nghe dữ liệu dạng HEX từ HC-12 (qua USB)...")
try:
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        timeout=1
    )
except serial.SerialException as e:
    print(f"Lỗi mở cổng serial: {e}")
    exit()

def is_valid_reading(temp, humi, fire):
    return (
        -20.0 <= temp <= 60.0 and
        5.0 <= humi <= 95.0 and
        0.0 <= fire <= 1.0
    )

from Datalink.DataProcessing import decode
from Saver import saveDataFromSTM32

while True:
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        hex_string = ' '.join(f'{b:02X}' for b in data)
        # print("Received (hex):", hex_string)

        try:
            temp, humi, fire = decode(data)

            if is_valid_reading(temp, humi, fire):
                continue

            print(f"Temp={temp}, Humi={humi}, Fire={fire}")
            saveDataFromSTM32(temp, humi, fire)

        except Exception as e:
            print("Lỗi giải mã:", e)

    time.sleep(0.1)
