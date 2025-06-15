import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "andresdamianvazquez")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:yzrVIkaNxcMiAsxhYcQJYnGEArulgJlo@metro.proxy.rlwy.net:34516/railway"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False