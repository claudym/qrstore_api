import os


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_ERROR_MESSAGE_KEY = "message"
    UPLOADED_PHOTOS_DEST = "static"
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
