from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_TOKEN_TIME_OUT_IN_MINUTES = os.getenv('JWT_TOKEN_TIME_OUT_IN_MINUTES')
    JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES = os.getenv('JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES')
    DEBUG = os.getenv('DEBUG')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')


db = SQLAlchemy()
