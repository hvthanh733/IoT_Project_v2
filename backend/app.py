from flask import Flask, redirect, url_for, render_template, session, request, jsonify, make_response
from dotenv import load_dotenv
import os
from flask import flash, get_flashed_messages
from flask_login import login_required
from functools import wraps
import jwt
import datetime
import re
from models.connect_db import db  # chỉ import db từ connect_db
from services.user_service import UserService

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ✅ Cấu hình SQLite hoặc database của bạn
basedir = os.path.abspath(os.path.dirname(__file__))  # đường dẫn tuyệt đối đến thư mục hiện tại (backend/)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'iot_system.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # kết nối app với SQLAlchemy
# Đăng ký blueprint

@app.route('/')
def default_route():
    return redirect(url_for('login_form'))
@app.route('/error')
def error():
    print("Đây là thông báo lỗi mẫu!")  # In ra console
    return "Lỗi đã được ghi log.", 200




@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username_signup = request.form.get('username_signup')
        password_signup = request.form.get('password_signup')
        phone_signup = request.form.get('phone_signup')
        email_signup = request.form.get('email_signup')

        exist_field = UserService.check_user_exists(username_signup, email_signup, phone_signup)
        if exist_field == "username":
            flash("Tên đăng nhập đã tồn tại, vui lòng chọn tên khác", "username_exist")
            return redirect(url_for('login_form'))
        elif exist_field == "email":
            flash("Email đã được đăng ký, vui lòng nhập email khác", "email_exist")
            return redirect(url_for('login_form'))
        elif exist_field == "phone":
            flash("Số điện thoại đã được đăng ký, vui lòng nhập số khác", "number_exist")
            return redirect(url_for('login_form'))


        new_user = UserService.create_user(username_signup, password_signup, email_signup, phone_signup)
        flash('Đã gửi yêu cầu tạo tài khoản đến admin', 'signup_successfull')
        return redirect(url_for('login_form'))

    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"username: {username}")
        print(f"password: {password}")

        success, user = UserService.login(username, password)
        print(f"success: {success}")
        print(f"user: {user}")
        if success:
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('user not found!', category="fail_login")
            return redirect(url_for('login_form'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    role = session.get('role', 'user')  # Mặc định là user nếu không có
    return render_template('user_management.html', role=role)



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"Error starting the app: {e}")

