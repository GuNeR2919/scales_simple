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
    WEIGHTS_PER_PAGE = 10

    SCALES_TITLE = 'Vehicle scales'
    SCALES_HOST = '192.168.2.70'
    SCALES_PORT = 4196
    SCALES_PATTERN = r'^\D*(\d*)kg'
    MINIMUM_FILTERED_WEIGHT = 1000
    WAIT_TIME = 10

    # SCALES_TITLE = 'Portable scales'
    # SCALES_HOST = '192.168.2.10'
    # SCALES_PORT = 11001
    # SCALES_PATTERN = r'^[0|w]*([^0|\D]\d*)\skg'
    # MINIMUM_FILTERED_WEIGHT = 100
    # WAIT_TIME = 10
