import os
import logging
from io import BytesIO
import pyvips
import numpy as np
from PIL import Image, ImageFile
from functools import lru_cache
import psutil
import shutil
from concurrent.futures import ThreadPoolExecutor
import threading

# Cho phép load ảnh bị cắt xén
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageProcessor:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ImageProcessor, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Khởi tạo các tham số xử lý ảnh"""
        # Giới hạn bộ nhớ sử dụng (MB)
        self.max_memory_mb = 400  # Để lại 100MB cho hệ thống
        self.chunk_size = 2048  # Kích thước mỗi chunk (pixel)
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        
        # Thiết lập bộ nhớ cho pyvips
        # pyvips.cache_set_max(0)  # Tắt cache để tiết kiệm bộ nhớ
        pyvips.cache_set_max_mem(50 * 1024 * 1024)  # Giới hạn cache 50MB
    
    @staticmethod
    def get_memory_usage():
        """Lấy thông tin sử dụng bộ nhớ hiện tại"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)  # MB
    
    def check_memory_available(self, required_mb=100):
        """Kiểm tra xem có đủ bộ nhớ không"""
        available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
        return available_memory > required_mb
    
    def process_large_image(self, input_path, output_path, max_dimension=9000, quality=85):
        """
        Xử lý ảnh lớn bằng cách sử dụng pyvips
        
        Args:
            input_path: Đường dẫn đến file ảnh đầu vào
            output_path: Đường dẫn lưu file ảnh đầu ra
            max_dimension: Kích thước tối đa (rộng hoặc cao)
            quality: Chất lượng ảnh đầu ra (0-100)
            
        Returns:
            dict: Thông tin về ảnh đã xử lý
        """
        try:
            # Kiểm tra bộ nhớ trước khi xử lý
            if not self.check_memory_available(200):  # Cần ít nhất 200MB trống
                raise MemoryError("Not enough memory to process this image")
            
            # Đọc ảnh với pyvips (sử dụng disk thay vì RAM)
            image = pyvips.Image.new_from_file(input_path, access='sequential')
            
            # Lấy thông số ảnh
            width, height = image.width, image.height
            
            # Tính tỷ lệ resize nếu cần
            scale = min(max_dimension / max(width, height), 1.0)
            
            # Nếu ảnh quá lớn, resize trước khi xử lý
            if scale < 1.0:
                image = image.resize(scale)
                width, height = image.width, image.height
            
            # Xử lý ảnh (có thể thêm các bước xử lý khác ở đây)
            # Ví dụ: chỉnh độ sáng, độ tương phản, v.v.
            
            # Lưu ảnh với chất lượng tối ưu
            image.write_to_file(
                output_path,
                Q=quality,
                strip=True,  # Xóa metadata không cần thiết
                optimize_coding=True,
                interlace=True
            )
            
            # Trả về thông tin ảnh đã xử lý
            return {
                'success': True,
                'width': width,
                'height': height,
                'size': os.path.getsize(output_path),
                'path': output_path
            }
            
        except Exception as e:
            logging.error(f"Error processing image: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_regions(self, image_path, regions, output_dir):
        """
        Cắt các vùng từ ảnh gốc
        
        Args:
            image_path: Đường dẫn đến ảnh gốc
            regions: Danh sách các vùng cần cắt [{'x': x, 'y': y, 'width': w, 'height': h}]
            output_paths: Đường dẫn lưu các ảnh đã cắt
            
        Returns:
            list: Danh sách đường dẫn đến các ảnh đã cắt
        """
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                
            # Đọc ảnh gốc
            image = pyvips.Image.new_from_file(image_path, access='sequential')
            
            results = []
            
            for i, region in enumerate(regions):
                # Tạo tên file đầu ra
                output_path = os.path.join(output_dir, f"region_{i+1}.jpg")
                
                # Cắt ảnh
                x, y = int(region['x']), int(region['y'])
                width, height = int(region['width']), int(region['height'])
                
                # Đảm bảo không vượt quá kích thước ảnh
                x = max(0, min(x, image.width - 1))
                y = max(0, min(y, image.height - 1))
                width = min(width, image.width - x)
                height = min(height, image.height - y)
                
                if width <= 0 or height <= 0:
                    results.append(None)
                    continue
                
                # Cắt và lưu ảnh
                region_img = image.crop(x, y, width, height)
                region_img.write_to_file(
                    output_path,
                    Q=90,
                    strip=True,
                    optimize_coding=True
                )
                
                results.append({
                    'path': output_path,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                })
            
            return results
            
        except Exception as e:
            logging.error(f"Error extracting regions: {str(e)}", exc_info=True)
            return []
    
    def cleanup_temp_files(self, *file_paths):
        """Xóa các file tạm"""
        def _delete_file(file_path):
            try:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path, ignore_errors=True)
                    else:
                        os.remove(file_path)
            except Exception as e:
                logging.warning(f"Could not delete {file_path}: {str(e)}")
        
        # Chạy trong thread riêng để không block request
        for file_path in file_paths:
            if file_path:  # Chỉ xử lý nếu đường dẫn không rỗng
                self.thread_pool.submit(_delete_file, file_path)

# Tạo instance toàn cục
image_processor = ImageProcessor()
