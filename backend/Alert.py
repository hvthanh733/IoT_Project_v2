import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import random
import string

def generate_random_password(length=5):
    characters = string.ascii_lowercase + string.digits  # chỉ chữ thường và số
    return ''.join(random.choices(characters, k=length))

load_dotenv()
sender_email = os.getenv("GMAIL_SEND_ALERT")
receiver_email_test = "hthanhjj0703@gmail.com"
password = os.getenv("PASSWORD_GMAIL_ALERT")


# --------------------------------------------------------------
# Sign Up Email
def send_signup_email(receiver_email, message):
    body = message
    subject = "IoT - Signup Confirmation"
    send_email_base(receiver_email, subject, body)
# --------------------------------------------------------------
# Password Recovery Email
def send_password_recovery_email(receiver_email):
    new_password = generate_random_password()
    body = f"Your new password is: {new_password}\n\nPlease change it after logging in."
    subject = "IoT - Password Recovery"
    send_email_base(receiver_email, subject, body)
    return new_password
# --------------------------------------------------------------
# Create User Email
def send_email_create_user(receiver_email):
    new_password = generate_random_password()
    body = f"Your new password is: {new_password}\n\nPlease change it after logging in."
    subject = "IoT - User Management"
    send_email_base(receiver_email, subject, body)
    return new_password
# --------------------------------------------------------------
# Genaral Alert Email
def send_email_alert(receiver_email ,message):
    body = message
    subject = "IoT - Notification"
    send_email_base(receiver_email, subject, body)
# --------------------------------------------------------------
# Threshold Email Temp / Humi - Fire
def send_email_threshold_temp(receiver_email, temp, TEMP_THRESH, now):
    subject = 'IoT - Temperature Over Threshold'
    body = f"""Warning - Temperature Over {TEMP_THRESH}!
    - Temperature: {temp}°C at {now}"""
    send_email_base2(receiver_email, subject, body)

def send_email_threshold_humi(receiver_email, humi, HUMI_THRESH, now):
    subject = 'IoT - Humidity Below Threshold'
    body = f"""Warning - Humidity Below {HUMI_THRESH}!
    - Humidity: {humi}% at {now}"""
    send_email_base2(receiver_email, subject, body)

def send_email_fuzzy(receiver_email, temp, humi, TEMP_THRESH, HUMI_THRESH, now):
    subject = 'IoT - FIRE DETECTED'
    body = f"""FIRE DETECTED
    - Temperature: {temp}°C (Threshold: {TEMP_THRESH})
    - Humidity: {humi}% (Threshold: {HUMI_THRESH})
    - Time: {now}"""
    send_email_base2(receiver_email, subject, body)
# --------------------------------------------------------------
# Alert Email Threshold
def send_email_threshold_all(receiver_email, temp_value, humi_value):
    subject = "IoT - Threshold Notification"
    body = f"""\
        The temperature and humidity thresholds have been changed to:
        - Temperature: {temp_value}°C
        - Humidity: {humi_value}%
        """
    send_email_base2(receiver_email, subject, body)

def send_email_base2(receiver_emails, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_emails, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print("Email sending error:", e)
# --------------------------------------------------------------
def send_email_base(receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print("Email sending error:", e)

