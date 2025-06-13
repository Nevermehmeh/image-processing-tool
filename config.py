import os
from pathlib import Path

# Đường dẫn gốc của dự án
BASE_DIR = Path(__file__).parent.absolute()

# Cấu hình cơ sở dữ liệu
class Config:
    SECRET_KEY = 'dev-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Giới hạn upload 16MB
    UPLOAD_EXTENSIONS = ['.png']
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_IMAGE_SIZE = 6000  # Kích thước tối đa của ảnh (pixel)
    
    # Thư mục upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'app', 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app', 'static')
    
    def __init__(self):
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
