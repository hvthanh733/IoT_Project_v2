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
# from flask_login import login_required, 
from functools import wraps
from flask_login import LoginManager,login_user
from flask import session, redirect, url_for
import time
# test
# from SensorData import value_all_blocks
# import SensorData

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
@login_required
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def default_route():
    session.clear()
    return redirect(url_for('login_form'))
    # return redirect(url_for('test_sensor'))
# source venv/bin/activate

# @app.route("/sensor_data12")
# def sensor_data12():
#     data = SensorData.value_all_blocks12()
#     return data

# @app.route("/sensor_data34")
# def sensor_data34():
#     data = SensorData.value_all_blocks34()
#     return data


@app.route('/test_sensor')
def test_sensor():
    return render_template('test.html')


@app.route('/dashboard')
def dashboard():
    if(session.get('user_id') != None):
        role = session.get('role', 'user')
        user_id = session.get('user_id')
        return render_template('dashboard.html', role=role, user_id=user_id)
    return redirect(url_for('login_form'))



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login_form'))


@app.route('/add_newusers', methods=['POST'])
def api_addnewusers():
    new_username = request.form.get('add_username')
    new_phone = request.form.get('add_phone')
    new_email = request.form.get('add_email')

    # Kiểm tra hợp lệ từng trường
    validations = [
        (UserService.validate_username(new_username), {
            "username_format": "Tên người dùng không đúng định dạng (chỉ chứa chữ/số, không quá 10 ký tự)",
            "username_space":  "Tên người dùng không được chứa khoảng trắng",
        }),
        (UserService.validate_phone(new_phone), {
            "phone_format": "Số điện thoại phải gồm đúng 10 chữ số",
            "phone_space":  "Số điện thoại không được chứa khoảng trắng",
        }),
        (UserService.validate_email(new_email), {
            "email_space": "Email không được chứa khoảng trắng",
        }),
    ]

    # Xử lý lỗi validation
    for result, messages in validations:
        if result != "ok":
            return jsonify({
                'success': False,
                'message': messages.get(result, "Dữ liệu điền không hợp lệ")
            })

    # Kiểm tra tồn tại
    exist_field = UserService.check_user_exists(new_username, new_phone, new_email)
    if exist_field:
        error_messages2 = {
            "username": "Tên người dùng đã tồn tại, vui lòng chọn tên khác",
            "phone":    "Số điện thoại đã được sử dụng",
            "email":    "Email đã được đăng ký",
        }
        return jsonify({
            'success': False,
            'message': error_messages2.get(exist_field, "Tài khoản đã tồn tại")
        })

    # Tạo người dùng
    created = UserService.add_newuser(new_username, new_phone, new_email)
    if created:
        return jsonify({'success': True, 'message': 'Thêm người dùng thành công'})
    
    return jsonify({'success': False, 'message': 'Không thể tạo người dùng'})

@app.route('/update_username', methods=['POST'])
def api_update_username():
    user_id = request.form.get('user_id')
    new_username = request.form.get('new_username')

    result = UserService.validate_username(new_username)
    if result != "ok":
        error_messages = {
            "username_format": "Tên người dùng không đúng định dạng (chỉ chứa chữ/số, tối đa 10 ký tự)",
            "username_space":  "Tên người dùng không được chứa khoảng trắng"
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Tên người dùng không hợp lệ")})

    success = UserService.update_username(user_id, new_username)
    if success:
        return jsonify({'success': True, 'message': 'Update thành công'})
    
    return jsonify({'success': False, 'message': 'Update không thành công'})

@app.route('/update_phone', methods=['POST'])
def api_update_phone():
    user_id = request.form.get('user_id')
    new_phone = request.form.get('new_phone')

    # Validate phone
    result = UserService.validate_phone(new_phone)
    if result != "ok":
        error_messages = {
            "phone_format": "Số điện thoại phải gồm đúng 10 chữ số",
            "phone_space":  "Số điện thoại không được chứa khoảng trắng"
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Số điện thoại không hợp lệ")})

    # Nếu hợp lệ, tiến hành cập nhật
    success = UserService.update_phone(user_id, new_phone)
    if success:
        return jsonify({'success': True, 'message': 'Update thành công'})
    
    return jsonify({'success': False, 'message': 'Update không thành công'})

@app.route('/update_email', methods=['POST'])
def api_update_email():
    user_id = request.form.get('user_id')
    new_email = request.form.get('new_email')

    result = UserService.validate_email(new_email)
    if result != "ok":
        error_messages = {
            "email_space": "Email không được chứa khoảng trắng",
            "email_format": "Email không đúng định dạng hợp lệ"
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Email không hợp lệ")})

    success = UserService.update_email(user_id, new_email)
    if success:
        return jsonify({'success': True, 'message': 'Update thành công'})
    
    return jsonify({'success': False, 'message': 'Update không thành công'})

@app.route('/update_password', methods=['POST'])
def api_update_password():
    user_id = request.form.get('user_id')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    # Validate định dạng mật khẩu mới
    validation_result = UserService.validate_password_format(new_password)
    if validation_result != "ok":
        error_messages = {
            "password_format": "Mật khẩu không đúng định dạng (chỉ chữ/số, tối đa 16 ký tự)",
            "password_space":  "Mật khẩu không được chứa khoảng trắng"
        }
        return jsonify({'success': False, 'message': error_messages.get(validation_result, "Mật khẩu không hợp lệ")})

    success = UserService.update_password(user_id, old_password, new_password)
    if success:
        return jsonify({'success': True, 'message': 'Update thành công'})

    return jsonify({'success': False, 'message': 'Update không thành công'})

@app.route('/api/users')
def api_users():
    keyword = request.args.get('keyword', '').strip()
    return UserService.get_users_by_type('user', keyword)


# Button alert
@app.route('/api/button_event', methods=['GET'])
def api_get_button_events():
    keyword = request.args.get('keyword', '').strip()
    return UserService.get_eventButton_by_type(keyword)

@app.route('/button_event_update_time_end', methods=['POST', 'DEL'])
def button_event_update_time_end():
    if request.method == 'POST':
        try:
            data = request.get_json()
            id = data.get("id")
            time_end = data.get("time_end")
            time_start = data.get("time_start")
            
            success = UserService.update_time_end(id, time_end, time_start)

            if success:
                return jsonify({"message": "Success"}), 200
            return jsonify({"message": "Fail"}), 422
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    if request.method == 'DEL':
        try:
            data = request.get_json()
            id = data.get("id")

            resp = UserService.del_date(id)
            if (resp):
                return jsonify({"message": "Success"}), 200
            return jsonify({"message": "Fail"}), 422
        except Exception as e:
            return jsonify({"error": str(e)}), 500
# Button alert


@app.route('/api/signup_queue')
def api_signup_queue():
    keyword = request.args.get('keyword', '').strip()
    return UserService.get_users_by_type('queue', keyword)

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

# @app.route('/api/user_info/<int:user_id>', methods=['GET'])
# def api_delete_user(user_id):
#     success, message = UserService.delete_user(user_id)

#     if success:
#         return jsonify({
#             'success': True,
#             'message': message
#         }), 200

#     return jsonify({
#         'success': False,
#         'message': message
#     }), 400
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

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    success, user = UserService.infor_user(user_id)
    if user:
        return jsonify({
            'success': True,
            'user': user
        }), 200

    return jsonify({
        'success': False,
        'message': user
    }), 400

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def api_change_username(user_id):

    data = request.get_json()
    new_username = data.get('new_username')
    message, success = UserService.change_username(new_username, user_id)
    if message:
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
        # username_forgot_password = request.form.get('username_forgot_password')
        email_forgot_password = request.form.get('email_forgot_password')

        result = UserService.check_email(email_forgot_password)
        print(result)
        if result:
            # result trả về (True, user_obj, email_obj) nếu tồn tại
            newpass = send_email_resetpass(email_forgot_password) 
            check = UserService.reset_newpassword(email_forgot_password, newpass)
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
        username = request.form.get('username_signup')
        password = request.form.get('password_signup')
        phone = request.form.get('phone_signup')
        email = request.form.get('email_signup')

        validation_errors = [
            (UserService.validate_username(username), {
                "username_format": ("Tên đăng nhập không đúng định dạng (chỉ chứa chữ/số, tối đa 10 ký tự, không dấu cách hoặc ký tự đặc biệt)", "username_error"),
                "username_space":  ("Tên đăng nhập không được chứa khoảng trắng", "username_space"),
            }),
            (UserService.validate_phone(phone), {
                "phone_format": ("Số điện thoại phải là số và đúng 10 chữ số", "phone_error"),
                "phone_space":  ("Số điện thoại không được chứa khoảng trắng", "phone_space"),
            }),
            (UserService.validate_email(email), {
                "email_space": ("Email không được chứa khoảng trắng", "email_space"),
                "email_format": ("Email không đúng định dạng hợp lệ", "email_format"),
            }),
            (UserService.validate_password_format(password), {
                "password_format": ("Mật khẩu không đúng định dạng (tối đa 16 ký tự, không dấu cách hoặc ký tự đặc biệt)", "password_error"),
                "password_space":  ("Mật khẩu không được chứa khoảng trắng", "password_space"),
            }),
        ]

        # Nếu có lỗi thì hiển thị flash và redirect
        for result, mapping in validation_errors:
            if result != "ok":
                msg, category = mapping.get(result, ("Lỗi không xác định", "error"))
                flash(msg, category)
                return redirect(url_for('sign_up'))

        # Kiểm tra trùng dữ liệu
        exists = UserService.check_user_exists(username, phone, email)
        exist_errors = {
            "username": ("Tên đăng nhập đã tồn tại, vui lòng chọn tên khác", "username_exist"),
            "email":    ("Email đã được đăng ký, vui lòng nhập email khác", "email_exist"),
            "phone":    ("Số điện thoại đã được đăng ký, vui lòng nhập số khác", "number_exist"),
        }

        if exists:
            msg, category = exist_errors.get(exists, ("Thông tin đã tồn tại", "exist_error"))
            flash(msg, category)
            return redirect(url_for('sign_up'))

        # Tạo user
        UserService.create_user(username, password, phone, email)
        flash('Đã gửi yêu cầu tạo tài khoản đến admin', 'signup_successfull')
        return redirect(url_for('sign_up'))

    return render_template('sign_up.html')





@app.route('/login', methods=['GET', 'POST'])
def login_form():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, user = UserService.login(username, password)
        if success:
            session['username'] = username
            session['role'] = user.role
            session['user_id'] = user.id
            print(user.id)
            return redirect(url_for('dashboard'))
        else:
            flash('user not found!', category="fail_login")

    return render_template('login.html')




if __name__ == '__main__':
    try:
        tailscale_output = subprocess.getoutput("tailscale ip")
        tailscale_ip = tailscale_output.splitlines()[0]

        print(f"http://{tailscale_ip}:8000")
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
       
    except Exception as e:
        print(f"Error starting the app: {e}")

