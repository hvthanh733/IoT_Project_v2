import pygame
import time
import os

def play_sound_loop_alert():
    file_path = "/home/thanh/Desktop/IoT_Project_v2/backend/sound_alert_fire.mp3"

    if not os.path.isfile(file_path):
        print(f"Sound not exists: {file_path}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
        print("Sound in 30 second...")

        time.sleep(30)

        pygame.mixer.music.stop()
        print("End Sound")

    except Exception as e:
        print(f"Error: {e}")

