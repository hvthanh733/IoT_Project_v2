from flask import Flask, redirect, url_for, render_template, session, request, jsonify
from dotenv import load_dotenv
import os
from flask_login import login_required
from functools import wraps
import jwt
import datetime
import re
from models.connect_db import db  # chỉ import db từ connect_db
from services.user_service import check_user_pass

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
    return redirect(url_for('sign_up'))
    
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        success, user = check_user_pass(username, password)
        if success:
            session['username'] = username
            session['role'] = user.role  # Gán role vào session

            return redirect(url_for('dashboard'))
        else:
            flash('Sai username hoặc mật khẩu')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    role = session.get('role', 'user')  # Mặc định là user nếu không có
    return render_template('test.html', role=role)



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"Error starting the app: {e}")

