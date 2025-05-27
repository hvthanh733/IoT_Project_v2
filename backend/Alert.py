import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "alertiotproject@gmail.com"
receiver_email = "hthanhjj0703@gmail.com"
password = "dvnj riqm rlvp cxyd" 

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Thử gửi email bằng Python"

body = "Nanh quả là đz"

message.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email đã được gửi thành công!")
except Exception as e:
    print("Có lỗi xảy ra:", e)