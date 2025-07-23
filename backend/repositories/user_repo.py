from models.model_project import SignUpQueue, User , FireEvent, SensorBlockProperty, SensorBlockPosition, Room
from models.connect_db import db
from services.password_hash import generate_password, verify_pass
from flask import jsonify, request
import sqlite3
from datetime import datetime, timedelta

class DataLogRepo:
    def save_start_time():
        now = datetime.now()
        today_str = now.date().isoformat()
        time_start_str = now.strftime("%H:%M:%S")

        existing_event = FireEvent.query.filter_by(status='active').first()
        if existing_event:
            return False 

        new_event = FireEvent(
            room_id=1,
            date=today_str,
            time_start=time_start_str,
            time_end=None,
            note="Fuzzy & Threshold Detect Fire",
            status="active"
        )
        db.session.add(new_event)
        db.session.commit()
        return True

    def save_end_time():
        now = datetime.now()
        time_end_str = now.strftime("%H:%M:%S")

        active_event = FireEvent.query.filter_by(status='active').first()
        if active_event:
            active_event.time_end = time_end_str
            active_event.status = 'inactive'
            db.session.commit()
            return True
        return False

    def get_alldays():
        return SensorBlockProperty.query.all()

    def save_datalog(max_temp, time_max_temp,
                    min_temp, time_min_temp,
                    max_humi, time_max_humi,
                    min_humi, time_min_humi):
        date_now = datetime.now().date()
        existing = SensorBlockProperty.query.filter_by(date=date_now).first()
        block = SensorBlockPosition.query.get(1)
        if existing:
            existing.block_id = block.id
            existing.max_temp = max_temp
            existing.time_max_temp = time_max_temp
            existing.min_temp = min_temp
            existing.time_min_temp = time_min_temp
            existing.max_humi = max_humi
            existing.time_max_humi = time_max_humi
            existing.min_humi = min_humi
            existing.time_min_humi = time_min_humi
        else:
            new_log = SensorBlockProperty(
                date=date_now,
                block_id=block.id,
                max_temp=max_temp,
                time_max_temp=time_max_temp,
                min_temp=min_temp,
                time_min_temp=time_min_temp,
                max_humi=max_humi,
                time_max_humi=time_max_humi,
                min_humi=min_humi,
                time_min_humi=time_min_humi,
            )
            db.session.add(new_log)
            
        db.session.commit()
        return True



class UserRepo:

    def infor_room_for_user(id):
        room = Room.query.filter_by(id=id).first()
        if room:
            return room.name_room, room.size_m2, room.x, room.y, room.z
        return None, None, None, None, None

    def get_all_email():
        users = User.query.all()
        
        # queued_users = SignUpQueue.query.all()
        
        emails = [u.email for u in users if u.email] 
                #  + \ [q.email for q in queued_users if q.email]

        return emails



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
            username = new_user.username
            db.session.add(new_user)
            db.session.commit()
            return True, username
        return False, None

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
            return new_user, new_user.email
        else:
            db.session.delete(user)
            db.session.commit()
            return True, None
    
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
            email = user.email
            db.session.delete(user)
            db.session.commit()
            return True, email
        return False, None

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
class RealTimeRepo():
    def get_node(node):
        return SensorBlockPosition.query.filter_by(node=node).all()

class ThresholdRepo():
    def threhold_byDay(date):
        threshold = SensorBlockProperty.query.filter_by(date=date).first()
        if threshold:
            return threshold.threshold_temp_alert, threshold.threshold_humi_alert
        return None, None
    # def threhold_temp(block_id):
    #     temp = SensorBlockProperty.query.filter_by(block_id=block_id).first()
    #     if temp:
    #         return temp.new_threshold_temp_alert
    #     return None

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

    def get_threshold():
        date_now = datetime.now().date()
        get_data_day = SensorBlockProperty.query.filter_by(date=date_now).first()
        
        if get_data_day:
            temp = get_data_day.threshold_temp_alert
            humi = get_data_day.threshold_humi_alert
            return temp, humi
        else:
            return None, None

    def get_id_temp_humi_day():
        date_now = datetime.now().date()
        get_data_day = SensorBlockProperty.query.filter_by(date=date_now).first()

        if get_data_day:
            id_day = get_data_day.id
            temp = get_data_day.threshold_temp_alert
            humi = get_data_day.threshold_humi_alert
            return id_day, temp, humi
        else:
            return None, None, None
    
    def set_default_threshold_case1(id_day, threshold_temp, threshold_humi):
        get_day = SensorBlockProperty.query.filter_by(id=id_day).first()
        if get_day:
            get_day.threshold_temp_alert = threshold_temp
            get_day.threshold_humi_alert = threshold_humi
            db.session.commit()
            return True
        return False
    
    def set_default_threshold_case2(id_day):
        current_day = SensorBlockProperty.query.filter_by(id=id_day).first()

        if not current_day:
            return False

        current_date = current_day.date

        prev_day_data = (
            SensorBlockProperty.query
            .filter(SensorBlockProperty.date < current_date)
            .order_by(SensorBlockProperty.date.desc())
            .first()
        )

        if prev_day_data:
            current_day.threshold_temp_alert = prev_day_data.threshold_temp_alert
            current_day.threshold_humi_alert = prev_day_data.threshold_humi_alert
            db.session.commit()
            return True

        return False

    def update_threshold(date_today, temp_value, humi_value):
        record = SensorBlockProperty.query.filter_by(date=date_today).first()
        if record:
            record.threshold_temp_alert = temp_value
            record.threshold_humi_alert = humi_value

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
