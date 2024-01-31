import os
from dotenv import load_dotenv

print('/config.py')

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEIGHTS_PER_PAGE = 20
    # SCALES_HOST = '192.168.6.18'
    # SCALES_PORT = 11001
    SCALES_HOST = '192.168.6.18'
    SCALES_PORT = 4196
