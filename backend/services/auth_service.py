from repositories.user_repository import get_user_by_username
from werkzeug.security import check_password_hash

def check_login(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user.password, password):
        return user
    return None
