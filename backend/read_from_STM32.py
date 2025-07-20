import serial
import threading
import time

from Datalink.DataProcessing import decode
from Saver import saveDataFromSTM32

latest_data = {"temp": None, "humi": None, "fire": None}

def is_valid_reading(temp, humi, fire):
    return (
        -20.0 <= temp <= 60.0 and
        5.0 <= humi <= 95.0 and
        0.0 <= fire <= 1.0
    )
key= {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f 
}
def listen_serial():
    global latest_data
    
    try:
        ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
        print("Open USB serial.")
    except serial.SerialException as e:
        print(f"Error open USB serial: {e}")
        return

    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            try:
                temp, humi, fire = decode(key, data)
                if is_valid_reading(temp, humi, fire):
                    latest_data["temp"] = temp
                    latest_data["humi"] = humi
                    latest_data["fire"] = fire

                    saveDataFromSTM32(temp, humi, fire)

                    print(f"Temp={temp}, Humi={humi}, Fire={fire}")
            except Exception as e:
                print("Error:", e)
        time.sleep(0.1)








# import serial
# import time
# from Datalink.DataProcessing import decode
# # from Saver import saveDataFromSTM32

# # latest_data = {"temp": None, "humi": None, "fire": None}
# key = {
#     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
#     0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
#     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
#     0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f 
# }

# def listen_serial():
#     # global latest_data
#     try:
#         ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)
#         print("Open USB serial.")
#     except serial.SerialException as e:
#         print(f"Error open USB serial: {e}")
#         return

#     while True:
#         if ser.in_waiting > 0:
#             data = ser.read(ser.in_waiting)
#             try:
#                 temp, humi, fire = decode(key, data)
#                 if is_valid_reading(temp, humi, fire):
#                     # latest_data["temp"] = temp
#                     # latest_data["humi"] = humi
#                     # latest_data["fire"] = fire
#                     # saveDataFromSTM32(temp, humi, fire)
#                     print("--------------------------")
#                     print(f"Temp={temp}")
#                     print(f"Humi={humi}")
#                     print(f"Fire={fire}")
#                     print("--------------------------")
#             except Exception as e:
#                 print("Error:", e)
#         time.sleep(0.1)

# # listen_serial()