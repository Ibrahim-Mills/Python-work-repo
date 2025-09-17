import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key
SECRET_KEY = 'your_secret_key'

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # or your preferred database URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
