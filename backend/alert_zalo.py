from zlapi import ZaloAPI
import json
import os

COOKIES_FILE = "cookies.json"

# Hàm đăng nhập nếu chưa có cookies
def login_and_save_cookies(phone, password, imei):
    bot = ZaloAPI(phone=phone, password=password, imei=imei)
    cookies = bot.getSessionCookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)
    return bot

# Hàm tải cookies từ file
def load_cookies():
    if not os.path.exists(COOKIES_FILE):
        return None
    with open(COOKIES_FILE, "r") as f:
        return json.load(f)

# Hàm chính gửi tin nhắn
def alertZalo():
    phone = "0923775005"  # Thay bằng số thật
    password = "vinahey309"  # Thay bằng mật khẩu thật
    imei = "123456789012345"  # Dùng IMEI bất kỳ (như một định danh giả lập)

    cookies = load_cookies()

    # Nếu có cookies, dùng lại
    if cookies:
        bot = ZaloAPI(session_cookies=cookies)
    else:
        # Nếu chưa có thì đăng nhập
        bot = login_and_save_cookies(phone, password, imei)

    # ✅ Lưu ý: Thay thế USER_ID bằng ID thật của người nhận!
    user_id = "ZALO_USER_ID_CẦN_GỬI"

    # Gửi tin nhắn
    bot.sendMessage(user_id=user_id, message="🚨 Cảnh báo IoT: Có nguy cơ cháy xảy ra!")

if __name__ == "__main__":
    alertZalo()
