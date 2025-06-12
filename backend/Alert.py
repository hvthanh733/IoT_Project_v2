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


def send_email_resetpass(receiver_email):
    newpassword = generate_random_password()

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email_test
    message["Subject"] = "IoT - Sending New Password"

    body = f"Your new password is: {newpassword}\n\nPlease change it after logging in."


    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email đã được gửi thành công!")
    except Exception as e:
        print("Có lỗi xảy ra:", e)
    return newpassword

# def readDatabase():

# def send_email_to_all()
# sender_email = os.getenv("GMAIL_ALERT")
# def send_email_notification(receiver_email, subject, body):
#     sender_email = "alertiotproject@gmail.com"
#     password = "dvnj riqm rlvp cxyd"  # App password từ Google

#     # Tạo nội dung email
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject

#     message.attach(MIMEText(body, "plain"))

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()  # Bắt đầu giao tiếp an toàn
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, message.as_string())
#             print("Email đã được gửi đến", receiver_email)
#     except Exception as e:
#         print("Lỗi khi gửi email:", e)


# def alertZalo():
#     bot = ZaloAPI(phone="0923775005", password="vinahey309", imei="IMEI", session_cookies=COOKIES)

#     friends = bot.getFriends()
#     for friend in friends:
#         print(friend["user_id"], "-", friend["display_name"])

# alertZalo()
