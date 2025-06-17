import os
from pathlib import Path

# Đường dẫn gốc của dự án
BASE_DIR = Path(__file__).parent.absolute()

# Cấu hình cơ sở dữ liệu
class Config:
    SECRET_KEY = 'dev-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Tăng giới hạn upload lên 50MB
    UPLOAD_EXTENSIONS = ['.png', '.jpg', '.jpeg']
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_IMAGE_SIZE = 9000  # Tăng kích thước tối đa lên 9000x9000px
    
    # Thư mục upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'app', 'templates')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app', 'static')
    
    def __init__(self):
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
