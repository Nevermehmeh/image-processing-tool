import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from app import create_app, db
from config import Config

def init_db():
    app = create_app(Config)
    with app.app_context():
        # Tạo tất cả các bảng
        db.create_all()
        print("Đã tạo xong cơ sở dữ liệu!")

if __name__ == '__main__':
    init_db()
