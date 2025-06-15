from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Tabla de asociación muchos-a-muchos entre usuarios y dispositivos
d_user_devices = db.Table(
    "user_devices",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("device_id", db.Integer, db.ForeignKey("devices.id"), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relación muchos-a-muchos con Device
    devices = db.relationship(
        "Device",
        secondary=d_user_devices,
        back_populates="users"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


    api_key = db.Column(db.String(64), unique=True, nullable=True, default=lambda: secrets.token_hex(32))
   


    # Relación inversa muchos-a-muchos con User
    users = db.relationship(
        "User",
        secondary=d_user_devices,
        back_populates="devices"
    )

    # Relación uno-a-muchos con Data
    data = db.relationship("Data", backref="device", lazy=True)

class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)

    # Campos adicionales para futuros datos (hasta 15)
    extra1 = db.Column(db.String(200), nullable=True)
    extra2 = db.Column(db.String(200), nullable=True)
    extra3 = db.Column(db.String(200), nullable=True)
    extra4 = db.Column(db.String(200), nullable=True)
    extra5 = db.Column(db.String(200), nullable=True)
    extra6 = db.Column(db.String(200), nullable=True)
    extra7 = db.Column(db.String(200), nullable=True)
    extra8 = db.Column(db.String(200), nullable=True)
    extra9 = db.Column(db.String(200), nullable=True)
    extra10 = db.Column(db.String(200), nullable=True)
    extra11 = db.Column(db.String(200), nullable=True)
    extra12 = db.Column(db.String(200), nullable=True)
    extra13 = db.Column(db.String(200), nullable=True)
    extra14 = db.Column(db.String(200), nullable=True)
    extra15 = db.Column(db.String(200), nullable=True)