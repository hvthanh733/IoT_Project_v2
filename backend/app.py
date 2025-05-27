from flask import Flask, redirect, url_for
from routes.admin import admin_bp
from routes.login import login_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)backend/services
app.secret_key =  os.getenv("SECRET_KEY")
print("SECRET_KEY =", os.getenv("SECRET_KEY"))

# Đăng ký blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(login_bp)

# Chuyển hướng vào login mặc định
@app.route('/')
def default_route():
    return redirect(url_for('login.login_form'))  # Mặc định chuyển hướng đến route login
    # return redirect(url_for())
# Khởi chạy ứng dụng
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"Error starting the app: {e}")
