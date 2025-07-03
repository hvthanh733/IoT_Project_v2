from flask import Flask, redirect, url_for, render_template, session, request, jsonify, make_response
from dotenv import load_dotenv
import os
from flask import flash, get_flashed_messages
from flask_login import login_required
from functools import wraps
import jwt
import datetime
from datetime import datetime, timedelta

import re
from models.connect_db import db
from services.user_service import UserService, DataLogService
import subprocess
from Alert import send_signup_email, send_password_recovery_email, send_email_threshold_all
from services.password_hash import generate_password, verify_pass
import sqlite3
from flask import jsonify, request
# from flask_login import login_required, 
from functools import wraps
from flask_login import LoginManager, login_user
from flask import session, redirect, url_for
import time
from Datalink.DataProcessing import decode
from Saver import read_CSV, delete_csv_file
from read_from_STM32 import listen_serial, latest_data
import threading
from alert_mechanism import SystemAlert
event_id = None

load_dotenv()

app = Flask(__name__)
serial_thread = threading.Thread(target=listen_serial, daemon=True)
serial_thread.start()

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



@app.route('/api/system_alert', methods=['POST'])
def api_system_alert():
    date_now = datetime.now().date()
    result = read_CSV()
    TEMP_THRESH, HUMI_THRESH = DataLogService.threhold_byDay(date_now)
    temp, _ = result['temperature']['max']
    humi, _ = result['humidity']['min']
    fire = result['fire_changes']
    check, all_emails = UserService.get_all_email()

    is_fire = SystemAlert(temp, humi, fire, TEMP_THRESH, HUMI_THRESH, all_emails)
    # is_fire = False
    if is_fire:
        created = DataLogService.save_start_time()
        if created:
            print("New event fire.")
    else:
        closed = DataLogService.save_end_time()
        if closed:
            print("End event fire.")

    return jsonify({"is_fire": is_fire})




# @app.route('/alert')
# def alert():
#     try:
#         result = readCSV()
#         print("result", result)

#         high_temp, time_high_temp = result
#         # 20
#         threshold_temp = UserService.check_threshold_temp(1)
        
#         if high_temp > threshold_temp:
#             id_event, check = UserService.get_time_start()
#             if check == True:
#                 delete_csv_file()
#             return jsonify({"status": "success", "message": "FIREE", "id": id_event})
            
#         return jsonify({"status": "normal", "message": "no Fire"})
#     except Exception as e:
#         return jsonify({"status": "false", "message": str(e)})
         
@app.route('/save_time_end')
def save_time_end():   
    try:
        id_event = request.args.get('id')
        print("id",id_event)
        check = UserService.get_time_end(id_event)
        if check == True:
            return jsonify({"status": "success", "message": "Save End Time Fire"})
        return jsonify({"status": "normal", "message": "Cant Save"})
    except Exception as e:
        return jsonify({"status": "false", "message": str(e)})


@app.route('/dashboard')
def dashboard():
    if(session.get('user_id') != None):
        role = session.get('role', 'user')
        user_id = session.get('user_id')
        nodes = UserService.get_node(1)
        
        # DataLogService.set_default_threshold(1, None, None)

        id_day, threshold_temp, threshold_humi = DataLogService.get_id_temp_humi_day()
        print(id_day)
        DataLogService.set_default_threshold(id_day, threshold_temp, threshold_humi)

        temp, humi = DataLogService.get_threshold()
        return render_template('dashboard.html', role=role, 
                                user_id=user_id,data=latest_data,
                                nodes=nodes,
                                threshold_temp_alert=temp,
                                threshold_humi_alert=humi)
    return redirect(url_for('login_form'))


@app.route('/api/save_data_day')
def api_save_data_day():
    result = read_CSV()
    if result:
        max_temp, max_temp_time = result['temperature']['max']
        min_temp, min_temp_time = result['temperature']['min']

        max_humi, max_humi_time = result['humidity']['max']
        min_humi, min_humi_time = result['humidity']['min']

        check = DataLogService.save_datalog(
            max_temp, max_temp_time,
            min_temp, min_temp_time,
            max_humi, max_humi_time,
            min_humi, min_humi_time
        )

        if check:
            print("Save succesful")

    return jsonify({"status": "success", "message": "Data saved"})


@app.route('/api/latest_data')
def api_latest_data():
    return jsonify(latest_data)

@app.route('/api/data_day')
def api_data_day():
    result = read_CSV()
    temp, humi = DataLogService.get_threshold()
    return jsonify({
        "data": result,
        "threshold_temp":temp,
        "threshold_humi":humi
    })


@app.route('/api/check_threshold')
def api_check_threshold():
    id_day, threshold_temp, threshold_humi = DataLogService.get_id_temp_humi_day()

    check = DataLogService.set_default_threshold(id_day, threshold_temp, threshold_humi)
    if check:
        return jsonify({"status": "success","message": "successful"})

    return jsonify({"status": "fail","message": "not successful"})

@app.route('/api/get_threshold', methods=['GET'])
def api_get_threshold():
    temp, humi = DataLogService.get_threshold()
    if temp is not None and humi is not None:
        return jsonify({
            "status": "success",
            "message": "Push Threshold Successful",
            "threshold_temp_alert": temp,
            "threshold_humi_alert": humi
        })
    return jsonify({
        "status": "fail",
        "message": "Push Threshold not successful"
    })

@app.route('/api/update_threshold', methods=['POST'])
def api_update_threshold():
    data = request.get_json()
    temp_value = data.get('temp')
    humi_value = data.get('humi')
    check, all_emails = UserService.get_all_email()
    print(all_emails)
    if temp_value is None or humi_value is None:

        return jsonify({
            "status": "fail",
            "message": "Missing temperature or humidity value"
        }), 400

    updated = DataLogService.update_threshold(temp_value, humi_value)
    
    if updated:
        if check:
            send_email_threshold_all(all_emails, temp_value, humi_value)
            return jsonify({
                "status": "success",
                "message": "Threshold updated successfully"
            })
    else:
        return jsonify({
            "status": "fail",
            "message": "Failed to update threshold"
        }), 500


@app.route("/api/get_all_properties", methods=["GET"])
def get_all_properties():
    days = DataLogService.get_alldays()
    print(days)
    result = []
    for day in days:
        result.append({
            "id": day.id,
            "date": str(day.date),
            "threshold_temp_alert": day.threshold_temp_alert,
            "threshold_humi_alert": day.threshold_humi_alert,
            "block_id": day.block_id,
            "max_temp": day.max_temp,
            "min_temp": day.min_temp,
            "max_humi": day.max_humi,
            "min_humi": day.min_humi,
            "time_max_temp": day.time_max_temp,
            "time_min_temp": day.time_min_temp,
            "time_max_humi": day.time_max_humi,
            "time_min_humi": day.time_min_humi
        })

    return jsonify(result)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login_form'))


@app.route('/update_username', methods=['POST'])
def api_update_username():
    user_id = request.form.get('user_id')
    new_username = request.form.get('new_username')

    result = UserService.validate_username(new_username)
    if result != "ok":
        error_messages = {
            "username_format": "Username is not in correct format (letters/numbers only, maximum 10 characters, no space)",
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Username not valid")})

    success = UserService.update_username(user_id, new_username)
    if success:
        return jsonify({'success': True, 'message': 'Update succesful'})
    
    return jsonify({'success': False, 'message': 'Update not succesful'})

@app.route('/update_phone', methods=['POST'])
def api_update_phone():
    user_id = request.form.get('user_id')
    new_phone = request.form.get('new_phone')

    # Validate phone
    result = UserService.validate_phone(new_phone)
    if result != "ok":
        error_messages = {
            "phone_format": "Phone number must consist of exactly 10 digits (no space)",
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Phone number not valid")})

    success = UserService.update_phone(user_id, new_phone)
    if success:
        return jsonify({'success': True, 'message': 'Update succesful'})
    
    return jsonify({'success': False, 'message': 'Update not succesful'})

@app.route('/update_email', methods=['POST'])
def api_update_email():
    user_id = request.form.get('user_id')
    new_email = request.form.get('new_email')

    result = UserService.validate_email(new_email)
    if result != "ok":
        error_messages = {
            "email_format": "Email is not in valid format"
        }
        return jsonify({'success': False, 'message': error_messages.get(result, "Email not valid")})

    success = UserService.update_email(user_id, new_email)
    if success:
        return jsonify({'success': True, 'message': 'Update succesful'})
    
    return jsonify({'success': False, 'message': 'Update not succesful'})

@app.route('/update_password', methods=['POST'])
def api_update_password():
    user_id = request.form.get('user_id')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    validation_result = UserService.validate_password_format(new_password)
    if validation_result != "ok":
        error_messages = {
            "password_format": "Password is not in correct format (letters/numbers only, maximum 16 characters, no space)"
        }
        return jsonify({'success': False, 'message': error_messages.get(validation_result, "Password not valid")})

    success = UserService.update_password(user_id, old_password, new_password)
    if success:
        return jsonify({'success': True, 'message': 'Update succesful'})

    return jsonify({'success': False, 'message': 'Update not succesful'})

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

#-------------------------------------------------------------------
# Sign Up Queue
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
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Real-time
# @app.route('/')
# @login_required
# def real_time_value():
#     return render_template('realtime.html', data=latest_data)

#-------------------------------------------------------------------


#-------------------------------------------------------------------
# Delete User
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


# Add New User
@app.route('/add_newusers', methods=['POST'])
def api_addnewusers():
    new_username = request.form.get('add_username')
    new_phone = request.form.get('add_phone')
    new_email = request.form.get('add_email')

    # Check all case with each input
    validations = [
        (UserService.validate_username(new_username), {
            "username_format": "Username is not in correct format (letters/numbers only, no more than 10 characters, no space)",
        }),
        (UserService.validate_phone(new_phone), {
            "phone_format": "Phone number must consist of exactly 10 digits, with no special characters or spaces",
        }),
        (UserService.validate_email(new_email), {
            "email_format": "Email must contain a valid domain and must not contain any spaces.",
        }),
    ]

    # Process error validation
    for result, messages in validations:
        if result != "ok":
            return jsonify({
                'success': False,
                'message': messages.get(result, "Invalid input data")
            })

    # Check exist
    exist_field = UserService.check_user_exists(new_username, new_phone, new_email)
    if exist_field:
        error_messages2 = {
            "username": "Username already exists, please choose another one",
            "phone":    "Phone number already in use",
            "email":    "Email has been registered",
        }
        return jsonify({
            'success': False,
            'message': error_messages2.get(exist_field, "Account already exists")
        })

    # Create new user
    created = UserService.add_newuser(new_username, new_phone, new_email)
    if created:
        return jsonify({'success': True, 'message': 'User added successfully'})
    
    return jsonify({'success': False, 'message': 'Unable to create user'})
#-------------------------------------------------------------------

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

#-------------------------------------------------------------------
# Password Recovery
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':

        email_forgot_password = request.form.get('email_forgot_password')

        truth_user = UserService.check_email_user(email_forgot_password)
        if truth_user:
            newpass = send_password_recovery_email(email_forgot_password)
            updated = UserService.reset_newpassword(email_forgot_password, newpass)
            if updated:
                flash("Send request recovery password successful", "reset_pass_successfull")
            else:
                flash("Send request recovery password not successful", "reset_fail_db")
        else:
            flash("The username does not exist or account in sign up queue", "wrong_user_or_pass")
        
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')
#-------------------------------------------------------------------


#-------------------------------------------------------------------
# Sign Up       DONE
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username_signup')
        password = request.form.get('password_signup')
        phone = request.form.get('phone_signup')
        email = request.form.get('email_signup')
        validation_errors = [
            (UserService.validate_username(username), {
                "username_format": ("Invalid name format (just text/number, max 10 character, no space or special character)", "username_error"),
            }),
            (UserService.validate_phone(phone), {
                "phone_format": ("The phone number must be numeric, exactly 10 digits long, and contain no spaces", "phone_error"),
            }),
            (UserService.validate_email(email), {
                "email_format": ("The email is not in a valid format or contains spaces", "email_format"),
            }),
            (UserService.validate_password_format(password), {
                "password_format": ("The password is not in a valid format (maximum 16 characters, no spaces or special characters)", "password_error"),
            }),
        ]

        for result, mapping in validation_errors:
            if result != "ok":
                msg, category = mapping.get(result, ("Unknown error", "error"))
                flash(msg, category)
                return redirect(url_for('sign_up'))

        exists = UserService.check_user_exists(username, phone, email)
        exist_errors = {
            "username": ("The username already exists. Please choose a different one", "username_exist"),
            "email":    ("The email has already been registered. Please enter a different one", "email_exist"),
            "phone":    ("The phone number has already been registered. Please enter a different one.", "number_exist"),
        }

        if exists:
            msg, category = exist_errors.get(exists, ("The information already exists", "exist_error"))
            flash(msg, category)
            return redirect(url_for('sign_up'))

        # Create user
        new_user = UserService.create_user(username, password, phone, email)
        if new_user:
            flash('Request register sent to admin', 'signup_successfull')
        
        return redirect(url_for('sign_up'))

    return render_template('sign_up.html')
#-------------------------------------------------------------------


#-------------------------------------------------------------------
# Login     DONE
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
#-------------------------------------------------------------------


if __name__ == '__main__':
    try:
        tailscale_output = subprocess.getoutput("tailscale ip")
        tailscale_ip = tailscale_output.splitlines()[0]

        print(f"http://{tailscale_ip}:8000")
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

    except Exception as e:
        print(f"Error starting the app: {e}")

