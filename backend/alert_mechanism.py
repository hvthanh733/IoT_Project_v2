from datetime import datetime, timedelta
from Saver import read_CSV
from Fuzzy_Logic import FuzzyLogic
from Alert import send_email_threshold_temp, send_email_threshold_humi, send_email_fuzzy

last_temp_alert_time = datetime.now() - timedelta(minutes=11)
last_humi_alert_time = datetime.now() - timedelta(minutes=11)
last_fuzzy = datetime.now() - timedelta(minutes=11)

is_fire_event_active = False

def SystemAlert(temp, humi, fire, TEMP_THRESH, HUMI_THRESH, all_emails):
    global last_temp_alert_time, last_humi_alert_time,last_fuzzy, is_fire_event_active
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    fuzzy_fire = FuzzyLogic(temp, humi, fire, TEMP_THRESH, HUMI_THRESH)
    if temp >= TEMP_THRESH and now - last_temp_alert_time >= timedelta(minutes=10):
        send_email_threshold_temp(all_emails, temp, TEMP_THRESH, formatted_time)
        last_temp_alert_time = now

    if humi <= HUMI_THRESH and now - last_humi_alert_time >= timedelta(minutes=10):
        send_email_threshold_humi(all_emails, humi, HUMI_THRESH, formatted_time)
        last_humi_alert_time = now

    if temp > TEMP_THRESH and humi < HUMI_THRESH and fuzzy_fire is True:
        if now - last_fuzzy >= timedelta(minutes=10):
            send_email_fuzzy(all_emails, temp, humi, TEMP_THRESH, HUMI_THRESH, formatted_time)
            last_fuzzy = now
            is_fire_event_active = True
        return True

    else:
        # if is_fire_event_active:
        #     is_fire_event_active = False
        return False