import jwt
import datetime
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from functools import wraps

# Tạo blueprint cho admin
admin_bp = Blueprint('admin', __name__)

# # Middleware để kiểm tra token
# def login_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if not session.get('logged_in'):
#             return redirect(url_for('login.login_form'))
#         return f(*args, **kwargs)
#     return wrapper

# # Route admin
# @admin_bp.route('/admin')
# @login_required  # Áp dụng middleware để kiểm tra đăng nhậ
def admin_page():
    return render_template('dashboard_admin.html')
    # if session.get('user_type') == 'admin':  # Kiểm tra user_type nếu cần
    #     return render_template('dashboard_admin.html')
    # else:
    #     return redirect(url_for('login.login_form'))

# # Route đăng xuất (POST)
# @admin_bp.route('/logout', methods=['POST'])
# def logout():
#     session.clear()  # Xóa hết session
#     return redirect(url_for('login.login_form'))  # Chuyển hướng về trang login