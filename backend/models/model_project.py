from flask_sqlalchemy import SQLAlchemy
from models.connect_db import db  # chỉ import db từ connect_db
class User(db.Model):
    __tablename__ = 'user'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(50), unique=True, nullable=False)  # nên tăng lên 50
    password    = db.Column(db.String(255), nullable=False)  # nên để String, không nên là Float!
    email       = db.Column(db.String(255))
    phone       = db.Column(db.String(20))
    role        = db.Column(db.String(20))