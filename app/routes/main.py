from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app, redirect, url_for
import os
from werkzeug.utils import secure_filename
from app.models.template import Template
from app import db
import cv2
import numpy as np
import uuid
from datetime import datetime
import traceback
from PIL import Image
import io

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_thumbnail(image_path, output_path, size=(200, 200)):
    """Tạo thumbnail từ ảnh gốc, hỗ trợ ảnh lớn"""
    try:
        # Tạo thư mục đích nếu chưa tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Mở ảnh gốc bằng PIL với tối ưu cho ảnh lớn
        from PIL import Image, ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        with Image.open(image_path) as img:
            # Chuyển sang chế độ RGB nếu ảnh ở chế độ RGBA
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Thay đổi kích thước ảnh với bộ lọc chất lượng cao
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Lưu ảnh thumbnail với chất lượng tốt
            img.save(output_path, 'JPEG', quality=85, optimize=True, progressive=True)
            
        return True
    except Exception as e:
        current_app.logger.error(f'Lỗi khi tạo thumbnail: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return False

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/templates')
def list_templates():
    current_app.logger.info('Accessing /templates route')
    try:
        templates = Template.query.order_by(Template.created_at.desc()).all()
        current_app.logger.info(f'Found {len(templates)} templates')
        for t in templates:
            current_app.logger.info(f'Template: id={t.id}, name={t.name}, created_at={t.created_at}')
        return render_template('templates.html', templates=templates)
    except Exception as e:
        current_app.logger.error(f'Error in list_templates: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return f"An error occurred: {str(e)}", 500

@bp.route('/create-template')
def create_template():
    return render_template('create_template.html')

@bp.route('/edit-template/<int:template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    template = Template.query.get_or_404(template_id)
    
    if request.method == 'POST':
        try:
            # Cập nhật thông tin template
            template.name = request.form.get('name', template.name)
            
            # Cập nhật thông tin vùng 1
            template.region1_x = int(request.form.get('region1_x', template.region1_x))
            template.region1_y = int(request.form.get('region1_y', template.region1_y))
            template.region1_width = int(request.form.get('region1_width', template.region1_width))
            template.region1_height = int(request.form.get('region1_height', template.region1_height))
            
            # Cập nhật thông tin vùng 2
            template.region2_x = int(request.form.get('region2_x', template.region2_x))
            template.region2_y = int(request.form.get('region2_y', template.region2_y))
            template.region2_width = int(request.form.get('region2_width', template.region2_width))
            template.region2_height = int(request.form.get('region2_height', template.region2_height))
            
            # Xử lý upload ảnh mới nếu có
            if 'template_image' in request.files:
                file = request.files['template_image']
                if file and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                    # Xóa ảnh cũ nếu tồn tại
                    if template.template_image_path:
                        try:
                            old_image = os.path.join(current_app.config['UPLOAD_FOLDER'], template.template_image_path)
                            if os.path.exists(old_image):
                                os.remove(old_image)
                        except Exception as e:
                            current_app.logger.error(f'Error deleting old image: {str(e)}')
                    
                    # Lưu ảnh mới
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(filepath)
                    
                    # Cập nhật đường dẫn ảnh
                    template.template_image_path = unique_filename
                    
                    # Tạo thumbnail
                    thumbnail_filename = f"thumb_{unique_filename}"
                    thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail_filename)
                    if create_thumbnail(filepath, thumbnail_path):
                        template.thumbnail_path = os.path.join('thumbnails', thumbnail_filename)
            
            db.session.commit()
            return redirect(url_for('main.list_templates'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error updating template: {str(e)}')
            current_app.logger.error(traceback.format_exc())
            return f"An error occurred: {str(e)}", 500
    
    # Nếu là GET request, hiển thị form chỉnh sửa
    return render_template('edit_template.html', template=template)

@bp.route('/extract-regions')
def extract_regions():
    templates = Template.query.all()
    return render_template('extract_regions.html', templates=templates)

@bp.route('/api/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    try:
        current_app.logger.info(f'Fetching template with ID: {template_id}')
        template = Template.query.get(template_id)
        
        if template is None:
            current_app.logger.error(f'Template not found with ID: {template_id}')
            return jsonify({'error': 'Template not found'}), 404
            
        current_app.logger.info(f'Found template: {template.name}')
        
        # Chuyển đổi đối tượng SQLAlchemy thành dictionary
        template_dict = {
            'id': template.id,
            'name': template.name,
            'region1_x': template.region1_x,
            'region1_y': template.region1_y,
            'region1_width': template.region1_width,
            'region1_height': template.region1_height,
            'region2_x': template.region2_x,
            'region2_y': template.region2_y,
            'region2_width': template.region2_width,
            'region2_height': template.region2_height,
            'template_image_path': template.template_image_path,
            'thumbnail_path': template.thumbnail_path,
            'created_at': template.created_at.isoformat() if template.created_at else None
        }
        
        current_app.logger.info('Template data prepared for JSON serialization')
        return jsonify(template_dict)
        
    except Exception as e:
        current_app.logger.error(f'Error in get_template: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@bp.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    try:
        if request.method == 'POST':
            current_app.logger.info('Nhận yêu cầu tạo template mới')
            
            if not request.is_json:
                current_app.logger.error('Yêu cầu không phải là JSON')
                return jsonify({'error': 'Request must be JSON'}), 400
                
            data = request.get_json()
            current_app.logger.info(f'Dữ liệu nhận được: {data.keys() if data else "No data"}')
            
            # Kiểm tra dữ liệu bắt buộc
            required_fields = ['name', 'region1', 'region2']
            for field in required_fields:
                if field not in data:
                    current_app.logger.error(f'Thiếu trường bắt buộc: {field}')
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Kiểm tra cấu trúc dữ liệu region
            for region in ['region1', 'region2']:
                if not all(key in data[region] for key in ['width', 'height', 'x', 'y']):
                    current_app.logger.error(f'Cấu trúc dữ liệu {region} không hợp lệ')
                    return jsonify({'error': f'Invalid {region} data structure'}), 400
            
            # Kiểm tra xem template đã tồn tại chưa
            existing_template = Template.query.filter_by(name=data['name']).first()
            if existing_template:
                current_app.logger.error(f'Template đã tồn tại: {data["name"]}')
                return jsonify({'error': 'Template with this name already exists'}), 400
            
            current_app.logger.info('Tạo đối tượng Template mới')
            # Tạo template mới
            template = Template(
                name=data['name'],
                region1_width=data['region1']['width'],
                region1_height=data['region1']['height'],
                region1_x=data['region1']['x'],
                region1_y=data['region1']['y'],
                region2_width=data['region2']['width'],
                region2_height=data['region2']['height'],
                region2_x=data['region2']['x'],
                region2_y=data['region2']['y']
            )
            current_app.logger.info('Đã tạo đối tượng Template')
            
            # Lưu ảnh template nếu có
            if 'image' in data and data['image']:
                try:
                    current_app.logger.info('Bắt đầu lưu ảnh template')
                    # Tạo thư mục nếu chưa tồn tại
                    upload_folder = current_app.config.get('UPLOAD_FOLDER')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Tạo tên file duy nhất
                    filename = f"template_{uuid.uuid4().hex}.png"
                    filepath = os.path.join(upload_folder, filename)
                    
                    # Lưu ảnh từ base64
                    import base64
                    image_data = data['image']
                    if ',' in image_data:
                        header, image_data = image_data.split(",", 1)
                    
                    img_data = base64.b64decode(image_data)
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    
                    template.template_image_path = filename
                    
                    # Tạo thumbnail
                    thumbnail_filename = f"thumb_{filename}"
                    thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnails', thumbnail_filename)
                    if create_thumbnail(filepath, thumbnail_path):
                        template.thumbnail_path = f"thumbnails/{thumbnail_filename}"
                    
                    current_app.logger.info(f'Đã lưu ảnh template: {filepath}')
                except Exception as e:
                    current_app.logger.error(f'Lỗi khi lưu ảnh template: {str(e)}')
                    current_app.logger.error(traceback.format_exc())
                    return jsonify({'error': 'Failed to save template image'}), 500
            
            # Lưu template vào database
            try:
                db.session.add(template)
                db.session.commit()
                current_app.logger.info(f'Đã lưu template thành công: {template.id}')
                return jsonify(template.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Lỗi khi lưu template vào database: {str(e)}')
                current_app.logger.error(traceback.format_exc())
                return jsonify({'error': 'Database error'}), 500
        
        # Xử lý GET request
        templates = Template.query.all()
        return jsonify([t.to_dict() for t in templates])
    
    except Exception as e:
        current_app.logger.error(f'Lỗi không xác định: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
        
        # Lưu ảnh template nếu có
        if 'image' in data and data['image']:
            try:
                # Tạo thư mục nếu chưa tồn tại
                upload_folder = current_app.config.get('UPLOAD_FOLDER')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Tạo tên file duy nhất
                filename = f"template_{uuid.uuid4().hex}.png"
                filepath = os.path.join(upload_folder, filename)
                
                # Lưu ảnh từ base64
                import base64
                if ',' in data['image']:
                    header, encoded = data['image'].split(",", 1)
                else:
                    encoded = data['image']
                
                img_data = base64.b64decode(encoded)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                
                template.template_image_path = filename
            except Exception as e:
                current_app.logger.error(f"Error saving template image: {str(e)}")
                import traceback
                current_app.logger.error(traceback.format_exc())
                return jsonify({'error': f'Error saving image: {str(e)}'}), 500
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify(template.to_dict()), 201
    
    # GET: Lấy danh sách templates
    templates = Template.query.all()
    return jsonify([t.to_dict() for t in templates])

@bp.route('/api/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename, current_app.config['UPLOAD_EXTENSIONS']):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Đọc ảnh bằng OpenCV
        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Lấy kích thước ảnh
        height, width = img.shape[:2]
        
        return jsonify({
            'filename': filename,
            'width': width,
            'height': height,
            'url': url_for('static', filename=f'uploads/{filename}')
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/api/extract-regions', methods=['POST'])
def extract_image_regions():
    try:
        current_app.logger.info('Bắt đầu xử lý extract regions')
        
        # Kiểm tra xem có file trong request không
        if 'file' not in request.files:
            current_app.logger.error('Không tìm thấy file trong request')
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        template_id = request.form.get('template_id')
        
        if not template_id:
            current_app.logger.error('Thiếu template_id')
            return jsonify({'error': 'Missing template_id'}), 400
            
        current_app.logger.info(f'Template ID: {template_id}')
        current_app.logger.info(f'File: {file.filename}')
        
        # Lấy thông tin template
        template = Template.query.get(template_id)
        if not template:
            current_app.logger.error(f'Không tìm thấy template với ID: {template_id}')
            return jsonify({'error': 'Template not found'}), 404
        
        # Lưu file tạm thời
        filename = secure_filename(file.filename)
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_' + filename)
        file.save(temp_path)
        current_app.logger.info(f'Đã lưu file tạm thời: {temp_path}')
        
        try:
            # Đọc ảnh bằng PIL để xử lý ảnh lớn hiệu quả hơn
            from PIL import Image, ImageFile
            # Cho phép tải ảnh lớn
            Image.MAX_IMAGE_PIXELS = 1000000000  # Tăng giới hạn kích thước ảnh
            ImageFile.LOAD_TRUNCATED_IMAGES = True  # Cho phép đọc ảnh bị lỗi nhỏ
            
            # Mở ảnh bằng PIL
            pil_img = Image.open(temp_path)
            
            # Kiểm tra kích thước ảnh
            width, height = pil_img.size
            max_size = 9000
            if width > max_size or height > max_size:
                raise ValueError(f'Kích thước ảnh vượt quá giới hạn cho phép ({max_size}x{max_size}px)')
                
            # Chuyển sang OpenCV để xử lý
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            del pil_img  # Giải phóng bộ nhớ
            
            if img is None:
                raise ValueError('Không thể đọc file ảnh')
                
            # Tạo thư mục output nếu chưa tồn tại
            output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Tạo tên file cho ảnh kết quả
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = f"{os.path.splitext(filename)[0]}_{timestamp}"
            
            # Chuyển đổi tọa độ thành số nguyên trước khi cắt ảnh
            # Vùng 1
            x1, y1 = int(round(template.region1_x)), int(round(template.region1_y))
            w1, h1 = int(round(template.region1_width)), int(round(template.region1_height))
            region1 = img[y1:y1+h1, x1:x1+w1]
            
            # Vùng 2
            x2, y2 = int(round(template.region2_x)), int(round(template.region2_y))
            w2, h2 = int(round(template.region2_width)), int(round(template.region2_height))
            region2 = img[y2:y2+h2, x2:x2+w2]
            
            # Lưu các vùng đã cắt
            region1_filename = f"{base_name}_region1.png"
            region2_filename = f"{base_name}_region2.png"
            region1_path = os.path.join(output_dir, region1_filename)
            region2_path = os.path.join(output_dir, region2_filename)
            
            cv2.imwrite(region1_path, region1)
            cv2.imwrite(region2_path, region2)
            
            # Tạo URL để truy cập ảnh
            base_url = request.host_url.rstrip('/')
            
            response_data = {
                'region1': {
                    'url': f"{base_url}/static/uploads/output/{region1_filename}",
                    'filename': region1_filename
                },
                'region2': {
                    'url': f"{base_url}/static/uploads/output/{region2_filename}",
                    'filename': region2_filename
                }
            }
            
            current_app.logger.info('Trích xuất thành công')
            current_app.logger.info(f'Kết quả: {response_data}')
            
            return jsonify(response_data)
            
        except Exception as e:
            current_app.logger.error(f'Lỗi khi xử lý ảnh: {str(e)}')
            current_app.logger.error(traceback.format_exc())
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
            
        finally:
            # Xóa file tạm
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    current_app.logger.info(f'Đã xóa file tạm: {temp_path}')
            except Exception as e:
                current_app.logger.error(f'Lỗi khi xóa file tạm: {str(e)}')
                
    except Exception as e:
        current_app.logger.error(f'Lỗi không xác định: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@bp.route('/api/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    try:
        current_app.logger.info(f'Deleting template with ID: {template_id}')
        template = Template.query.get(template_id)
        
        if template is None:
            current_app.logger.error(f'Template not found with ID: {template_id}')
            return jsonify({'error': 'Template not found'}), 404
        
        # Xóa file ảnh gốc nếu tồn tại
        if template.template_image_path:
            try:
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], template.template_image_path)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    current_app.logger.info(f'Deleted image file: {image_path}')
            except Exception as e:
                current_app.logger.error(f'Error deleting image file: {str(e)}')
        
        # Xóa thumbnail nếu tồn tại
        if template.thumbnail_path:
            try:
                thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], template.thumbnail_path)
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
                    current_app.logger.info(f'Deleted thumbnail file: {thumbnail_path}')
            except Exception as e:
                current_app.logger.error(f'Error deleting thumbnail file: {str(e)}')
        
        # Xóa bản ghi trong database
        db.session.delete(template)
        db.session.commit()
        
        current_app.logger.info(f'Successfully deleted template with ID: {template_id}')
        return jsonify({
            'message': f'Template "{template.name}" đã được xóa thành công',
            'success': True
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting template: {str(e)}')
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Lỗi khi xóa template: {str(e)}',
            'success': False
        }), 500

@bp.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/static/uploads/output/<path:filename>')
def output_file(filename):
    output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output')
    return send_from_directory(output_dir, filename)
