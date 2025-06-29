from models.model_project import SignUpQueue, User , FireEvent, SensorBlockProperty
from models.connect_db import db
from services.password_hash import generate_password, verify_pass
from flask import jsonify, request
import sqlite3

class UserRepo:
    def get_user_by_id(id: int):
        user = User.query.filter_by(id=id).first()
        user_queue = SignUpQueue.query.filter_by(id=id).first()
        return user_queue or user

    def get_user_by_username(username: str):
        user = User.query.filter_by(username=username).first()
        user_queue = SignUpQueue.query.filter_by(username=username).first()
        return user or user_queue

    def get_user_by_username_login(username: str):
        user = User.query.filter_by(username=username).first()
        return user

    def get_user_by_email(email: str):
        user = User.query.filter_by(email=email).first()
        user_queue = SignUpQueue.query.filter_by(email=email).first()
        return user or user_queue

    def get_user_by_phone(phone: str):
        user = User.query.filter_by(phone=phone).first()
        user_queue = SignUpQueue.query.filter_by(phone=phone).first()
        return user or user_queue
    
    def create_user(username_signup: str, password: str, phone_signup: str, email_signup: str):
        new_user = SignUpQueue(username=username_signup, password=password, phone=phone_signup, email=email_signup,role="user",approved=False)
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return True
        return False

    def add_newuser(new_username: str, password_hashed: str, new_phone: str,  new_email: str):
        new_user = User(username=new_username, password=password_hashed, phone=new_phone, email=new_email,role="user")
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return True
        return False

    def updateUserQueue(user: SignUpQueue, is_accepted: bool):
        if is_accepted:
            new_user = User(username=user.username, password=user.password, email=user.email, phone=user.phone, role=user.role)
            db.session.delete(user)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        else:
            db.session.delete(user)
            db.session.commit()
            return True
    
    def reset_password(email: str, newpassword: str):
        user = User.query.filter_by(email=email).first()
        print(f"Resetting password for user: {user}")
        if user:
            return True
        user.password = newpassword
        db.session.commit()
        return False

    
    def delete_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def infor_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return {
                'id': user.id,
                # 'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'username': user.username
            }
            return user
        return None
    
    def change_username(new_username: str, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.username = new_username
            db.session.commit()
            return True
        return False

    def update_username(user_id: str, new_username: str):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.username = new_username
            db.session.commit()
            return True
        return False
    
    def update_phone(user_id: str, new_phonenumber: str):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.phone = new_phonenumber
            db.session.commit()
            return True
        return False
    
    def update_email(user_id: str, new_email: str):
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.email = new_email
            db.session.commit()
            return True
        return False
    
    def update_password(user_id, old_password: str, new_password: str):
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return False

        if generate_password(old_password) != user.password:
            return False 

        user.password = generate_password(new_password)
        db.session.commit()
        return True

    def search_users(user_type, keyword):
        keyword = keyword.strip()

        if user_type == 'queue':
            query = SignUpQueue.query
            if keyword:
                query = query.filter(SignUpQueue.username.like(f"%{keyword}%"))
        else:
            query = User.query.filter(User.role != 'admin')
            if keyword:
                query = query.filter(User.username.like(f"%{keyword}%"))

        results = query.all()

        user_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone
        } for user in results]

        return jsonify({'users': user_list})

    # Button alert
    def search_eventButton(keyword):
        keyword = keyword.strip()
        query = FireEvent.query
        query = query.filter(FireEvent.date.like(f"%{keyword}%"))

        results = query.all()

        event_list = [{
            'id': event.id,
            'date': event.date,
            'time_start': event.time_start,
            'time_end': event.time_end,
            'note': event.note,

        } for event in results]

        return jsonify({'events': event_list})

    def update_time_end(id, time_end):
        event = FireEvent.query.filter_by(id=id).first()
        if event and event.time_end:
            event.time_end = time_end
            db.session.commit()
            return True
        return False

    def del_time(id):
        event = FireEvent.query.filter_by(id=id).first()
        if (event):
            db.session.delete(event)
            db.session.commit()
            return True
        return False

class ThresholdRepo():
    def threhold_temp(block_id):
        temp = SensorBlockProperty.query.filter_by(block_id=block_id).first()
        if temp:
            return temp.threshold_temp_alert
        return None

    def get_time_start(today, start_time):
        new_event = FireEvent(date=today, time_start=start_time, time_end=None, note="hehe")
        db.session.add(new_event)
        db.session.commit()
        return new_event.id,True
    
    def get_time_end(id, today, end_time):
        full_end_time = f"{today} {end_time}"
        event = FireEvent.query.filter_by(id=id).first()
        if event:
            event.time_end = full_end_time
            db.session.commit()
            return True
        return False


    # def threhold_humi(block_id):
    #     prop = SensorBlockProperty.query.filter_by(block_id=block_id).first()
    #     if prop:
    #         return prop.threshold_humi_alert
    #     return None
    
    # def save_event(date, time_start, time_end=None, note=None):
    #     try:
    #         event = FireEvent(
    #             date=date,
    #             time_start=time_start,
    #             time_end=time_end,
    #             note=note
    #         )
    #         db.session.add(event)
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         print(f"[DB ERROR] Failed to save FireEvent: {e}")
    #         return False


    # def save_end_time_alert(date, time_end):
    #     try:
    #         event = FireEvent.query.filter_by(date=date, time_end=None).order_by(FireEvent.id.desc()).first()
    #         if event:
    #             event.time_end = time_end
    #             db.session.commit()
    #             return True
    #         return False
    #     except Exception as e:
    #         print("Lỗi khi lưu time_end:", e)
    #         return False
