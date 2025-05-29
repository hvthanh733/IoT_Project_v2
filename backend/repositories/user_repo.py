from models.model_project import User
from app import db

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    return None
     
def get_user_by_email(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    return None

def get_user_by_phone(phone: str):
    user = User.query.filter_by(phone=phone).first()
    if user:
        return user
    return None

def create_user(username_signup, password, email_signup, phone_signup):
    new_user = User(username=username_signup, password=password, phone=phone_signup, email=email_signup,role="user")
    db.session.add(new_user)
    db.session.commit()
