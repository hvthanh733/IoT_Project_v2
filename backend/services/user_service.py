from repositories.user_repo import UserRepo
from models.model_project import User
from services.password_hash import generate_password, verify_pass
import re

# Class UserService handle logic
class UserService:
    def login(username:str, password:str):
        user = UserRepo.get_user_by_username(username)
        # Check user in database table "user"
        if user is None:
            return False, None
        print(user)
        print(password)
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

    def validate_user_input(username: str, password: str, phone: str, email: str):
        # Length check
        if len(username) > 10:
            return "username_format"
        if len(password) > 16:
            return "password_format"
        if len(phone) > 10:
            return "phone_format"

        # Whitespace check
        if ' ' in username:
            return "username_space"
        if ' ' in password:
            return "password_space"
        if ' ' in phone:
            return "phone_space"
        if ' ' in email:
            return "email_space"

        # Regex format check
        if not re.fullmatch(r"[A-Za-z0-9]+", username):
            return "username_format"
        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            return "password_format"
        if not re.fullmatch(r"\d{1,10}", phone):  # Only digits
            return "phone_format"
        return "ok"


    # Function for forgot_password part
    def check_user_email(username: str, email: str):
        # Check the exist of user and email
        if not username or not email:
            return None

        check_user = UserRepo.get_user_by_username(username)
        check_email = UserRepo.get_user_by_email(email)  # Chỗ này phải gọi get_user_by_email chứ không phải get_user_by_username(email)

        # if username and email are true -> return True
        if check_user and check_email:
            return True, check_user, check_email
        return None

    # Create user form sign_up form
    def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str) -> bool:
        password_hashed = generate_password(password)
        UserRepo.create_user(username_signup, password_hashed, email_signup, phone_signup)
    
    def reset_newpassword(username: str, email: str, newpassword: str) -> bool:
        password_hashed = generate_password(newpassword)
        return UserRepo.reset_password(username, email,password_hashed)
