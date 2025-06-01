from models.model_project import SignUpQueue, User 
from models.connect_db import db
from services.password_hash import generate_password, verify_pass

class UserRepo:
    # UserRepo.py

    def get_user_by_username(username: str):
        user = User.query.filter_by(username=username).first()
        user_queue = SignUpQueue.query.filter_by(username=username).first()
        return user or user_queue

    def get_user_by_email(email: str):
        user = User.query.filter_by(email=email).first()
        user_queue = SignUpQueue.query.filter_by(email=email).first()
        return user or user_queue

    def get_user_by_phone(phone: str):
        user = User.query.filter_by(phone=phone).first()
        user_queue = SignUpQueue.query.filter_by(phone=phone).first()
        return user or user_queue

    def create_user(username_signup: str, password: str, email_signup: str, phone_signup: str):
        password_hashed = generate_password(password)
        new_user = SignUpQueue(username=username_signup, password=password, phone=phone_signup, email=email_signup,role="user",approved=False)
        # new_user = User(username=username_signup, password=password_hashed, phone=phone_signup, email=email_signup,role="user")
        db.session.add(new_user)
        db.session.commit()

    def reset_password(username: str, email: str, newpassword: str):
        user = User.query.filter_by(username=username, email=email).first()
        if not user:
            return False
        user.password = newpassword
        db.session.commit()
        return True

