import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zlapi import ZaloAPI
load_dotenv()
# sender_email = "alertiotproject@gmail.com"
# receiver_email = "hthanhjj0703@gmail.com"
# password = "dvnj riqm rlvp cxyd" 

# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = "Thử gửi email bằng Python"

# body = "Nanh quả là đz"

# message.attach(MIMEText(body, "plain"))

# try:
#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls() 
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         print("Email đã được gửi thành công!")
# except Exception as e:
#     print("Có lỗi xảy ra:", e)
sender_email = os.getenv("GMAIL_ALERT")
def send_email_notification(receiver_email, subject, body):
    sender_email = "alertiotproject@gmail.com"
    password = "dvnj riqm rlvp cxyd"  # App password từ Google

    # Tạo nội dung email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Bắt đầu giao tiếp an toàn
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("✅ Email đã được gửi đến", receiver_email)
    except Exception as e:
        print("❌ Lỗi khi gửi email:", e)


def alertZalo():
    bot = ZaloAPI(phone="0923775005", password="MẬT_KHẨU", imei="IMEI", session_cookies=COOKIES)
    bot.sendMessage(user_id="USER_ID", message="Nội dung tin nhắn")
