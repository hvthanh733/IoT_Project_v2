import jwt
import datetime
import re
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from functools import wraps

login_bp = Blueprint('login', __name__)  # Định nghĩa Blueprint cho login

# Đăng nhập và tạo JWT token
@login_bp.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra định dạng mật khẩu
        if not re.match("^[A-Za-z0-9]+$", password):
            return f"<script>alert('Mật khẩu không được chứa ký tự đặc biệt'); window.location.href='/login';</script>"

        if len(password) > 10:
            return f"<script>alert('Mật khẩu không được dài quá 10 ký tự'); window.location.href='/login';</script>"

        # Gộp kiểm tra tài khoản hoặc mật khẩu sai
        if username != 'admin' or password != '1':
            return f"<script>alert('Tài khoản hoặc mật khẩu không hợp lệ'); window.location.href='/login';</script>"

        # Đăng nhập thành công
        session['logged_in'] = True
        session['user_type'] = 'admin'
        return redirect(url_for('admin.admin_page'))

    return render_template('login.html')
