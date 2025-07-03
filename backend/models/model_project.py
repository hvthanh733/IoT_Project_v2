from flask_sqlalchemy import SQLAlchemy
from models.connect_db import db
from datetime import date
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
class FireEvent(db.Model):
    __tablename__ = 'fire_event' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    date = db.Column(db.String, nullable=False)
    time_start = db.Column(db.String, nullable=False)
    time_end = db.Column(db.String, nullable=True)
    note = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True, default='active')

    # Relationship
    # room = db.relationship("Room", backref="fire_events")

class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_room = db.Column(db.String, unique=True, nullable=False)
    size_m2 = db.Column(db.Float)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationship
    user = db.relationship("User", backref="rooms")

class SensorBlockPosition(db.Model):
    __tablename__ = 'sensor_block_position'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    node = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)

class SensorBlockProperty(db.Model):
    __tablename__ = 'sensor_block_property'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    block_id = db.Column(db.Integer, db.ForeignKey('sensor_block_position.id'))

    date = db.Column(db.Date, default=date.today)

    sensor_type1 = db.Column(db.String, default="DHT11")
    sensor_type2 = db.Column(db.String, default="KY-026")

    # Default threshold 
    threshold_temp_alert = db.Column(db.Float)
    threshold_humi_alert = db.Column(db.Float)

    # Logging max/min
    max_temp = db.Column(db.Float)
    time_max_temp = db.Column(db.String)

    min_temp = db.Column(db.Float)
    time_min_temp = db.Column(db.String)

    max_humi = db.Column(db.Float)
    time_max_humi = db.Column(db.String)

    min_humi = db.Column(db.Float)
    time_min_humi = db.Column(db.String)