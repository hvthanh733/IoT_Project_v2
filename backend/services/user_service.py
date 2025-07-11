from repositories.user_repo import UserRepo, ThresholdRepo, RealTimeRepo, DataLogRepo
from models.model_project import User
from services.password_hash import generate_password, verify_pass
import re
from Alert import send_password_recovery_email, send_signup_email, send_email_alert,send_email_create_user
from datetime import datetime
class DataLogService:
    def save_start_time():
        return DataLogRepo.save_start_time()

    def save_end_time():
        return DataLogRepo.save_end_time()

    def threhold_byDay(date_now):
        temp, humi = ThresholdRepo.threhold_byDay(date_now)
        return temp, humi
    
    def save_datalog(max_temp, max_temp_time,
                    min_temp, min_temp_time,
                    max_humi, max_humi_time,
                    min_humi, min_humi_time):
        check = DataLogRepo.save_datalog(max_temp, max_temp_time,
                                        min_temp, min_temp_time,
                                        max_humi, max_humi_time,
                                        min_humi, min_humi_time)
        if check:
            return True
        return False

    def get_alldays():
        return DataLogRepo.get_alldays()
    
    def get_threshold():
        temp, humi = ThresholdRepo.get_threshold()
        return temp, humi
    
    def update_threshold(temp_value, humi_value):
        date_today = datetime.now().date()
        update_threshold = ThresholdRepo.update_threshold(date_today, temp_value, humi_value)
        if update_threshold:
            return True
        return False

    def get_id_temp_humi_day():
        id_day, threshold_temp, threshold_humi = ThresholdRepo.get_id_temp_humi_day()
        return id_day, threshold_temp, threshold_humi

    def set_default_threshold(id_day, threshold_temp, threshold_humi):
        all_days = DataLogRepo.get_alldays()
        first_day = next((day for day in all_days if day.id == 1), None)

        if first_day and id_day == 1 and threshold_temp is None and threshold_humi is None:
            threshold_temp = 40
            threshold_humi = 30
            return ThresholdRepo.set_default_threshold_case1(id_day, threshold_temp, threshold_humi)

        elif id_day != 1 and threshold_temp is None and threshold_humi is None:
            return ThresholdRepo.set_default_threshold_case2(id_day)

        return False



# Class UserService handle logic
class UserService:
    def infor_room_for_user(id):
        name_room, size_m2, x, y, z = UserRepo.infor_room_for_user(id)
        return name_room, size_m2, x, y, z
    #-------------------------------------------------------------------
    # Get All Email
    def get_all_email():
        emails = UserRepo.get_all_email()
        if emails:
            return True, emails
        return False, None
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    # Login
    def login(username:str, password:str):
        user = UserRepo.get_user_by_username_login(username)
        # Check user in database table "user"
        if user is None:
            return False, None
        # check password hashed with the password of user in database
        if verify_pass(password, user.password):
            return True, user
        return False, None
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    # Get Node
    def get_node(node):
        return RealTimeRepo.get_node(node)
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    # Check username, password, phone, email
    def check_user_exists(username: str, phone: str, email: str):
        # Check if the username, email, or phone already exists in the database
        if not username:
            return None
        if UserRepo.get_user_by_username(username):
            return "username"
        if UserRepo.get_user_by_phone(phone):
            return "phone"
        if UserRepo.get_user_by_email(email):
            return "email"
        return None

    def validate_username(username: str):
        if (len(username) > 10) or (' ' in username) or not re.fullmatch(r"[A-Za-z0-9]+", username):
            return "username_format"
        return "ok"

    def validate_phone(phone: str):
        if (len(phone) != 10) or (' ' in phone) or not re.fullmatch(r"\d{10}", phone):
            return "phone_format"
        return "ok"

    def validate_email(email: str):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if (' ' in email) or not re.match(pattern, email):
            return "email_format"
        return "ok"

    def validate_password_format(password: str):
        if (len(password) > 16) or (' ' in password) or not re.fullmatch(r"[A-Za-z0-9]+", password):
            return "password_format"
        return "ok"
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    # Function for forgot_password part
    def check_email(email: str):
        # Check the exist of user and email
        if not email:
            return None

        check_email = UserRepo.get_user_by_email(email)

        # if username and email are true -> return True
        if check_email:
            return True, check_email
        return None
    #-------------------------------------------------------------------





    #-------------------------------------------------------------------
    # Create user form sign_up form
    def create_user(username_signup: str, password: str, phone_signup: str, email_signup: str) -> bool:
        password_hashed = generate_password(password)
        new_user, get_username = UserRepo.create_user(username_signup, password_hashed, phone_signup, email_signup)
        if new_user:
            send_signup_email(email_signup, f"Hi {get_username}, your account is sign up successful!")
            return True
        return False
    #-------------------------------------------------------------------


    #-------------------------------------------------------------------
    # Password Recover
    def reset_newpassword(email: str, newpassword: str) -> bool:
        password_hashed = generate_password(newpassword)
        return UserRepo.reset_password(email, password_hashed)

    def check_email_user(email: str) -> bool:
        user = User.query.filter_by(email=email).first()
        return user is not None
    #-------------------------------------------------------------------




    #-------------------------------------------------------------------
    # User Manager
    def updateUserQueue(userId, isAccepted):
        user = UserRepo.get_user_by_id(userId)
        get_username = user.username
        newUser, email = UserRepo.updateUserQueue(user, isAccepted)
        if email:
            send_email_alert(email, f"Hi {get_username}, your account is approval by Admin!")
        else: 
            send_email_alert(email, f"Hi {get_username}, your account is not approval by Admin!")

        return newUser

    def delete_user(user_id):
        user, email = UserRepo.delete_user(user_id)
        message = ""
        print(email)
        if user:
            message = "Delete successfully"
            send_email_alert(email, "Your account is deleted by admin")
        else:
            message = "Error while delete"
        return user, message

    def infor_user(user_id):
        user = UserRepo.infor_user(user_id)
        message = ""
        if user:
            message = "Show infor successfully"
        else:
            message = "Error while show infor"
        return message, user

    def change_username(new_username:str, user_id):
        success = UserRepo.change_username(new_username, user_id)
        message = ""
        if success:
            message = "Change username successfully"
        else:
            message = "Error while change username"
        return message, success

    def add_newuser(new_username: str,  new_phone: str, new_email: str) -> bool:
        newpass = send_email_create_user(new_email)
        password_hashed = generate_password(newpass)
        new_user = UserRepo.add_newuser(new_username , password_hashed, new_phone, new_email)
        return new_user
    #-------------------------------------------------------------------




    #-------------------------------------------------------------------
    # Edit Actor Information 
    def update_username(userid, new_username:str) -> bool:
        user = UserRepo.update_username(userid, new_username)
        return user

    def update_phone(userid, new_phonenumber:str) -> bool:
        user = UserRepo.update_phone(userid, new_phonenumber)
        return user

    def update_password(userid, old_password:str, new_password:str) -> bool:
        user = UserRepo.update_password(userid, old_password, new_password)
        return user

    def update_email(userid, new_email:str) -> bool:
        user = UserRepo.update_email(userid, new_email)
        return user
    #-------------------------------------------------------------------









    def get_users_by_type(user_type, keyword):
        return UserRepo.search_users(user_type, keyword)

    # Button event
    def get_eventButton_by_type(keyword):
        return UserRepo.search_eventButton(keyword)

    def update_time_end(id, time_end, time_start):
        check = False
        if (time_end > time_start):
            check = UserRepo.update_time_end(id, time_end)
            check=True
        elif (time_end <= time_start):
            pass
        return check
    
    def del_date(id):
        resp = UserRepo.del_time(id)
        return resp

    def check_threshold_temp(id):
        take_threshold_temp = ThresholdRepo.threhold_temp(id)
        return take_threshold_temp

    def get_time_start():
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        take_id , check = ThresholdRepo.get_time_start(today, current_time)
        return take_id, check

    def get_time_end(id_event):
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        return ThresholdRepo.get_time_end(id_event, today, current_time)
    #     take_threshold_temp = ThresholdRepo.threhold_temp(id)
    #     take_threshold_humi = ThresholdRepo.threhold_humi(id)
    #     alert_temp = None
    #     alert_humi = None
    #     mix_alert = False
    #     if high_temp > take_threshold_temp:
    #         alert_temp = high_temp

    #     if low_humi < take_threshold_humi:
    #         alert_humi = low_humi

    #     if high_temp > take_threshold_temp and low_humi < take_threshold_humi:
    #         mix_alert = True
    #     return alert_temp, alert_humi, mix_alert
    
    # def saveLogFireEvent(high_temp, time_high_temp) -> bool:
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     note = f"Fire > Threshold ({high_temp}°C)"
    #     return ThresholdRepo.save_event(today, time_high_temp, None, note)

    # def saveLogHumiEvent(low_humi, time_low_humi) -> bool:
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     note = f"Humi < Threshold ({low_humi}%)"
    #     return ThresholdRepo.save_event(today, time_low_humi, None, note)

    # def saveLogMixEvent(high_temp, time_high_temp, low_humi, time_low_humi) -> bool:
    #     today = datetime.now().strftime("%Y-%m-%d")
    #     note = f"Fire > {high_temp}°C & Humi < {low_humi}%"
    #     return ThresholdRepo.save_event(today, time_high_temp, None, note)

    # def save_end_time_alert():
    #     now = datetime.now()
    #     time_end = now.strftime("%H:%M:%S")
    #     date = now.strftime("%Y-%m-%d")
    #     return ThresholdRepo.save_end_time_alert(date, time_end)


