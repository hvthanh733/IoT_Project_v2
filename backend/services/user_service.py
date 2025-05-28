from repositories.user_repo import get_user_by_username

def check_user_pass(username, password):
    user = get_user_by_username(username)
    if user and user.password == password:
        return True, user
    return False, None
