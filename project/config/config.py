from utils import utils

ENV = 'development'
DEBUG = True
TESTING = True
HOST = 'http://localhost:'
PORT = 5000
SECRET_KEY = utils.generate_random_key()
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/db.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = './judge/tests'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt'])