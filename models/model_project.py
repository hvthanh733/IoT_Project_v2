from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Room(db.Model):
    __tablename__ = 'room'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_room   = db.Column(db.String(255), unique=True, nullable=False)
    size_m2     = db.Column(db.Float)
    sensor_positions = db.relationship("SensorBlockPosition", backref="room", lazy=True)


class SensorBlockPosition(db.Model):
    __tablename__ = 'sensor_block_position'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id     = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    x           = db.Column(db.Integer, nullable=False)
    y           = db.Column(db.Integer, nullable=False)


class SensorBlockProperty(db.Model):
    __tablename__ = 'sensor_block_property'
    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    block_name          = db.Column(db.String(255), unique=True)

    sensor_type1        = db.Column(db.String(100))
    coverage_sensor1    = db.Column(db.Float)
    sensor_type2        = db.Column(db.String(100))
    coverage_sensor2    = db.Column(db.Float)

    threshold_temp_max  = db.Column(db.Float)
    threshold_temp_min  = db.Column(db.Float)
    threshold_humi_max  = db.Column(db.Float)
    threshold_humi_min  = db.Column(db.Float)

    alert_fire = db.Column(db.String(100))


class SensorBlockData(db.Model):
    __tablename__ = 'sensor_block_data'
    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)

    block_id            = db.Column(db.Integer)  # Có thể ForeignKey nếu có bảng `sensor_block`
    date                = db.Column(db.DateTime)

    max_temp            = db.Column(db.Float)
    min_temp            = db.Column(db.Float)
    time_max_temp       = db.Column(db.Time)
    time_min_temp       = db.Column(db.Time)

    max_humi            = db.Column(db.Float)
    min_humi            = db.Column(db.Float)
    time_max_humi       = db.Column(db.Time)
    time_min_humi       = db.Column(db.Time)

    fire_state          = db.Column(db.Boolean)
    fire_state_human    = db.Column(db.Boolean)
    start_time          = db.Column(db.Time)
    end_time            = db.Column(db.Time)
