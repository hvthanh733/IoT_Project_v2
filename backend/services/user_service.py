from repositories import user_repo
from utils import pass_controller


def check_user_pass(username, password):
    user = user_repo.get_user_by_username(username)
    if user and verify_password(password, user.password):
        return True, user
    return False, None


def check_user_exists(username, email, phone):
    if not username:
        return None
    if user_repo.get_user_by_username(username):
        return "username"
    if user_repo.get_user_by_email(email):
        return "email"
    if user_repo.get_user_by_phone(phone):
        return "phone"
    return None


def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str) -> bool:
    # if (user_repo.get_user_by_email(email_signup) != None):
    #     return "Email already used"
    
    # if (user_repo.get_user_by_username(username_signup) != None):
    #     return "Username already exists"
    password_hashed = pass_controller.hash_password(password)
    user_repo.create_user(username_signup, password_hashed, email_signup, phone_signup)