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

def send_signup_email(receiver_email):
    body = "Your request for registration was sent successfully."
    subject = "IoT - Signup Confirmation"
    send_email_base(receiver_email, subject, body)

def send_password_recovery_email(receiver_email):
    new_password = generate_random_password()
    body = f"Your new password is: {new_password}\n\nPlease change it after logging in."
    subject = "IoT - Password Recovery"
    send_email_base(receiver_email, subject, body)
    return new_password


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


# def send_email(receiver_email, note):
#     newpassword = generate_random_password()
#     if note == "sign up message":
#         body = "Your request for register is send successful"
#     if note == "password recovery":
#         body = f"Your new password is: {newpassword}\n\nPlease change it after logging in."

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = "IoT - Sending New Password"


#     message.attach(MIMEText(body, "plain"))
    
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls() 
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email_test, message.as_string())
#             print("Email send succesfully!")
#     except Exception as e:
#         print("Error:", e)
#     return newpassword

