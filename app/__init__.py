from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback
from .filters import register_filters

# Khởi tạo các extension
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Tạo cấu hình
    config = config_class()
    
    # Tạo ứng dụng Flask
    app = Flask(__name__, 
                static_folder=config.STATIC_FOLDER,
                template_folder=config.TEMPLATE_FOLDER)
    
    # Cấu hình ứng dụng
    app.config.from_object(config)
    
    # Cấu hình logging
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Cấu hình file log
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10240,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Xóa các handler cũ nếu có
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App started')
    app.logger.info(f'Log file: {log_file}')
    
    # Log cấu hình
    app.logger.info(f'UPLOAD_FOLDER: {app.config["UPLOAD_FOLDER"]}')
    app.logger.info(f'DATABASE_URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    
    # Khởi tạo các extension
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Tạo thư mục tải lên nếu chưa tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails'), exist_ok=True)
    
    # Tạo bảng cơ sở dữ liệu
    with app.app_context():
        db.create_all()
    
    # Đăng ký blueprint
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Xử lý lỗi 404
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'404 Error: {error}')
        return jsonify({'error': 'Not found'}), 404
    
    # Xử lý lỗi 500
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'500 Error: {error}')
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
    
    # Đăng ký các filter
    register_filters(app)
    
    return app
