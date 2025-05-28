from models.model_project import User

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    return None
     
    # def get_user_by_email(mail: str) -> User:

    # def get_user_by_phone(phone: str)


