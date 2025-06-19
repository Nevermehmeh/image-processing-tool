import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'outputs')
    TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'temp')
    
    # Ensure upload and output directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    
    # Allowed file extensions
    UPLOAD_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    
    # Image processing settings
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 9000))  # pixels
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    
    # Performance settings
    THREADS_PER_PAGE = 2
    
    # Redis settings (for Celery, if needed)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery settings (if needed)
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE') or 'app.log'

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # In production, these should be set via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

# Dictionary to map config names to classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
