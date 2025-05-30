from models.model_project import SignUpQueue, User 
from models.connect_db import db

class UserRepo:
    def get_user_by_username(username: str):
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

    def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str):
        new_user = SignUpQueue(username=username_signup, password=password, phone=phone_signup, email=email_signup,role="user",approved=False)
        db.session.add(new_user)
        db.session.commit()
