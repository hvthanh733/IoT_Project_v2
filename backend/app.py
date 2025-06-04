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
import subprocess
from Alert import send_email_resetpass
from services.password_hash import generate_password, verify_pass
import sqlite3
from flask import jsonify, request
from flask_login import login_required, LoginManager

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login_form'

app.secret_key = os.getenv("SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'iot_system.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def default_route():
    return redirect(url_for('login_form'))

@login_required
@app.route('/dashboard')
def dashboard():
    role = session.get('role', 'user')
    return render_template('dashboard.html', role=role)

# @app.route('/')
# def default_route():
#     session['role'] = 'admin'  # Gán role luôn ở đây
#     return redirect(url_for('dashboard'))

# @app.route('/dashboard')
# def dashboard():
#     role = session.get('role', 'user')  # Lấy role từ session
#     return render_template('dashboard.html', role=role)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_form'))


@login_required
@app.route('/api/users')
def api_users():
    keyword = request.args.get('keyword', '').strip()
    return UserService.get_users_by_type('user', keyword)

@login_required
@app.route('/api/signup_queue')
def api_signup_queue():
    keyword = request.args.get('keyword', '').strip()
    return UserService.get_users_by_type('queue', keyword)

@login_required
@app.route('/api/userAccept', methods=['POST'])
def api_userAccept():
    data = request.get_json()
    user_id = data.get('userId')
    is_accepted = data.get('isAccepted')

    userService = UserService.updateUserQueue(user_id, is_accepted)
    if (userService):
        return jsonify({
            'success': True,
            'message': 'Update user success'
        })
    return jsonify({
        'success': False,
        'message': "Error while update status account"
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    success, message = UserService.delete_user(user_id)

    if success:
        return jsonify({
            'success': True,
            'message': message
        }), 200

    return jsonify({
        'success': False,
        'message': message
    }), 400


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username_forgot_password = request.form.get('username_forgot_password')
        email_forgot_password = request.form.get('email_forgot_password')

        result = UserService.check_user_email(username_forgot_password, email_forgot_password)
        print(result)
        if result:
            # result trả về (True, user_obj, email_obj) nếu tồn tại
            newpass = send_email_resetpass(username_forgot_password, email_forgot_password) 
            check = UserService.reset_newpassword(username_forgot_password, email_forgot_password, newpass)
            if check:
                flash("Đã gửi yêu cầu thay đổi mật khẩu thành công", "reset_pass_successfull")
            else:
                flash("Đã gửi email nhưng không lưu được mật khẩu mới", "reset_fail_db")
        else:
            flash("Username hoặc email không tồn tại", "wrong_user_or_pass")
        
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username_signup = request.form.get('username_signup')
        password_signup = request.form.get('password_signup')
        phone_signup = request.form.get('phone_signup')
        email_signup = request.form.get('email_signup')

        # Validate input format
        valid = UserService.validate_user_input(username_signup, password_signup, phone_signup, email_signup)
        if valid != "ok":
            if valid == "username_format":
                flash("Tên đăng nhập không đúng định dạng (chỉ chứa chữ/số, tối đa 10 ký tự, không dấu cách hoặc ký tự đặc biệt)", "username_error")
            elif valid == "password_format":
                flash("Mật khẩu không đúng định dạng (tối đa 16 ký tự, không dấu cách hoặc ký tự đặc biệt)", "password_error")
            elif valid == "phone_format":
                flash("Số điện thoại phải là số và tối đa 10 chữ số", "phone_error")
            
            elif valid == "username_space":
                flash("Tên đăng nhập không được chứa khoảng trắng", "username_space")
            elif valid == "password_space":
                flash("Mật khẩu không được chứa khoảng trắng", "password_space")
            elif valid == "phone_space":
                flash("Số điện thoại không được chứa khoảng trắng", "phone_space")
            elif valid == "email_space":
                flash("Email không được chứa khoảng trắng", "email_space")
            return redirect(url_for('sign_up'))

        # Check if exists
        exist_field = UserService.check_user_exists(username_signup, phone_signup, email_signup)

        if exist_field == "username":
            flash("Tên đăng nhập đã tồn tại, vui lòng chọn tên khác", "username_exist")
            return redirect(url_for('sign_up'))
        elif exist_field == "email":
            flash("Email đã được đăng ký, vui lòng nhập email khác", "email_exist")
            return redirect(url_for('sign_up'))
        elif exist_field == "phone":
            flash("Số điện thoại đã được đăng ký, vui lòng nhập số khác", "number_exist")
            return redirect(url_for('sign_up'))
        else:
            UserService.create_user(username_signup, password_signup, phone_signup, email_signup)
            flash('Đã gửi yêu cầu tạo tài khoản đến admin', 'signup_successfull')
            return redirect(url_for('sign_up'))

        return redirect(url_for('sign_up'))

    return render_template('sign_up.html')



@app.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, user = UserService.login(username, password)
        if success:
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('user not found!', category="fail_login")
            return redirect(url_for('login_form'))

    return render_template('login.html')




if __name__ == '__main__':
    try:
        tailscale_output = subprocess.getoutput("tailscale ip")
        tailscale_ip = tailscale_output.splitlines()[0]

        print(f"http://{tailscale_ip}:8000")
        app.run(host='0.0.0.0', port=8000, debug=True)
       
    except Exception as e:
        print(f"Error starting the app: {e}")

