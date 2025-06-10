from flask_sqlalchemy import SQLAlchemy
from models.connect_db import db

# This class defines the structure and attribute of the Users table and in the database.
class User(db.Model):
    __tablename__ = 'user'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(10), unique=True, nullable=False)
    password    = db.Column(db.String(16), nullable=False)
    email       = db.Column(db.String(100))
    phone       = db.Column(db.String(10))
    role = db.Column(db.String(20), nullable=False)

# This class defines the structure and attribute of the SignUpQueue table and in the database.
class SignUpQueue(db.Model):
    __tablename__ = 'sign_up_queue'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    email    = db.Column(db.String(100))
    phone    = db.Column(db.String(10))
    role     = db.Column(db.String(20), nullable=False, default='user')
    approved = db.Column(db.Boolean, default=False)

# This class defines the structure and attribute of the ButtonAlertEvent table and in the database.
class ButtonAlertEvent(db.Model):
    __tablename__ = 'button_alert' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String, nullable=False)
    time_start = db.Column(db.String, nullable=False)
    time_end = db.Column(db.String, nullable=True)
    note = db.Column(db.String, nullable=True)