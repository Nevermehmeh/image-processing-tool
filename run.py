#!/usr/bin/env python3
"""
Chạy ứng dụng trong môi trường phát triển.

Cấu hình mặc định:
- Host: 0.0.0.0 (chấp nhận kết nối từ mọi địa chỉ IP)
- Port: 5000
- Chế độ debug: Bật
- Auto-reload: Bật
"""
import os
import sys
import argparse
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

def parse_arguments():
    """Phân tích các tham số dòng lệnh."""
    parser = argparse.ArgumentParser(description='Chạy ứng dụng Image Processor')
    parser.add_argument(
        '--host', 
        type=str, 
        default=os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
        help='Địa chỉ host để chạy máy chủ (mặc định: 0.0.0.0)'
    )
    parser.add_argument(
        '--port', 
        type=int, 
        default=int(os.getenv('FLASK_RUN_PORT', 5000)),
        help='Cổng để chạy máy chủ (mặc định: 5000)'
    )
    parser.add_argument(
        '--no-debug', 
        action='store_false', 
        dest='debug',
        default=os.getenv('FLASK_DEBUG', 'true').lower() == 'true',
        help='Tắt chế độ debug'
    )
    parser.add_argument(
        '--no-reload', 
        action='store_false', 
        dest='reloader',
        default=True,
        help='Tắt tự động tải lại khi code thay đổi'
    )
    return parser.parse_args()

def main():
    """Hàm chính để khởi chạy ứng dụng."""
    # Phân tích tham số dòng lệnh
    args = parse_arguments()
    
    # Tạo ứng dụng Flask
    from app import create_app
    
    # Tạo ứng dụng với cấu hình phát triển
    app = create_app('development' if args.debug else 'production')
    
    # In thông tin cấu hình
    print("\n" + "="*50)
    print(f"Chạy ứng dụng tại: http://{args.host}:{args.port}")
    print(f"Chế độ debug: {'BẬT' if args.debug else 'TẮT'}")
    print(f"Tự động tải lại: {'BẬT' if args.reloader else 'TẮT'}")
    print("="*50 + "\n")
    
    # Chạy ứng dụng
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        use_reloader=args.reloader,
        threaded=True
    )

if __name__ == '__main__':
    main()
