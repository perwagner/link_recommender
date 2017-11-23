import os
from os.path import join, dirname
import datetime


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    ENV = os.environ.get('ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://tester:12345@db/LINKDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    DEBUG = True


config = {
    'local': LocalConfig
}