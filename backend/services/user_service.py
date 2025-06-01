from repositories.user_repo import UserRepo
from models.model_project import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def check_user_pass(username: str, password: str):
        user = UserRepo.get_user_by_username(username)
        if user and check_password_hash(password, user.password):
            return True, user
        return False, None

    def login(username:str, password:str):
        user = UserRepo.get_user_by_username(username)
        print(f"user repo: {user}")
        print(f"check: {check_password_hash(user.password, password)}")
        if (user == None):
            return "Uername not found", 404
            
        if (check_password_hash(user.password, password)):
            return True, user
        return "Login fail"

    def check_user_exists(username: str, email: str, phone: str):
        if not username:
            return None
        if UserRepo.get_user_by_username(username):
            return "username"
        if UserRepo.get_user_by_email(email):
            return "email"
        if UserRepo.get_user_by_phone(phone):
            return "phone"
        return None

    def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str) -> bool:
        password_hashed = generate_password_hash(password)
        UserRepo.create_user(username_signup, password_hashed, email_signup, phone_signup)