from repositories.user_repo import UserRepo
from models.model_project import User
from services.password_hash import generate_password, verify_pass
import re
from Alert import send_email_resetpass

# Class UserService handle logic
class UserService:
    def login(username:str, password:str):
        user = UserRepo.get_user_by_username(username)
        # Check user in database table "user"
        if user is None:
            return False, None
        # check password hashed with the password of user in database
        if verify_pass(password, user.password):
            return True, user
        return False, None
    
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

    
    def validate_user_fields(username: str, phone: str, email: str):
        if len(username) > 10:
            return "username_format"
        if len(phone) != 10:
            return "phone_format"

        if ' ' in username:
            return "username_space"
        if ' ' in phone:
            return "phone_space"
        if ' ' in email:
            return "email_space"

        if not re.fullmatch(r"[A-Za-z0-9]+", username):
            return "username_format"
        if not re.fullmatch(r"\d{1,10}", phone):
            return "phone_format"

        return "ok"

    def validate_password_format(password: str):
        if len(password) > 16:
            return "password_format"
        if ' ' in password:
            return "password_space"
        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            return "password_format"
        return "ok"

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

    # Create user form sign_up form
    def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str) -> bool:
        password_hashed = generate_password(password)
        UserRepo.create_user(username_signup, password_hashed, email_signup, phone_signup)
    
    def reset_newpassword(email: str, newpassword: str) -> bool:
        password_hashed = generate_password(newpassword)
        return UserRepo.reset_password(email, password_hashed)

   
    def get_users_by_type(user_type, keyword):
        return UserRepo.search_users(user_type, keyword)

    def updateUserQueue(userId, isAccepted):
        user = UserRepo.get_user_by_id(userId)
        newUser = UserRepo.updateUserQueue(user, isAccepted)
        return newUser

    def delete_user(user_id):
        user = UserRepo.delete_user(user_id)
        message = ""
        if user:
            message = "Delete successfully"
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
        newpass = send_email_resetpass(new_email)
        password_hashed = generate_password(newpass)
        new_user = UserRepo.add_newuser(new_username , password_hashed, new_phone, new_email)
        return new_user


    def update_username(userid, new_username:str) -> bool:
        user = UserRepo.update_username(userid, new_username)
        return user

    def update_phone(userid, new_phonenumber:str) -> bool:
        user = UserRepo.update_phone(userid, new_phonenumber)
        return user

    def update_password(userid, old_password:str, new_password:str) -> bool:
        user = UserRepo.update_password(userid, old_password, new_password)
        return user