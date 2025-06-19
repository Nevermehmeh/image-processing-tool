import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config
from .filters import register_filters

# Khởi tạo các extension
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Tạo và cấu hình ứng dụng Flask"""
    # Tạo ứng dụng Flask
    app = Flask(__name__)
    
    # Tải cấu hình
    app.config.from_object(config[config_name])
    
    # Đảm bảo các thư mục cần thiết tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
    
    # Cấu hình logging
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app.config.get('LOG_LEVEL', 'INFO'))
    
    # Xóa các handler cũ nếu có
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config.get('LOG_LEVEL', 'INFO'))
    
    # Ghi log khi khởi động
    app.logger.info('App starting...')
    app.logger.info(f'Upload folder: {app.config["UPLOAD_FOLDER"]}')
    app.logger.info(f'Output folder: {app.config["OUTPUT_FOLDER"]}')
    app.logger.info(f'Temp folder: {app.config["TEMP_FOLDER"]}')
    app.logger.info(f'Max image size: {app.config["MAX_IMAGE_SIZE"]}px')
    app.logger.info(f'Max content length: {app.config["MAX_CONTENT_LENGTH"] / (1024*1024):.1f}MB')
    
    # Khởi tạo các extension
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Đăng ký các blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Đăng ký các filter
    register_filters(app)
    
    # Xử lý lỗi 404
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404
    
    # Xử lý lỗi 500
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
    # Xử lý lỗi 413 (Request Entity Too Large)
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'error': f'File is too large. Maximum size is {app.config["MAX_CONTENT_LENGTH"] / (1024*1024):.1f}MB.'
        }), 413
    
    app.logger.info('App started successfully')
    
    return app
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
