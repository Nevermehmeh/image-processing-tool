from datetime import datetime
from app import db

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Thông tin vùng 1
    region1_width = db.Column(db.Integer, nullable=False)
    region1_height = db.Column(db.Integer, nullable=False)
    region1_x = db.Column(db.Integer, nullable=False)
    region1_y = db.Column(db.Integer, nullable=False)
    
    # Thông tin vùng 2
    region2_width = db.Column(db.Integer, nullable=False)
    region2_height = db.Column(db.Integer, nullable=False)
    region2_x = db.Column(db.Integer, nullable=False)
    region2_y = db.Column(db.Integer, nullable=False)
    
    # Đường dẫn đến file ảnh template và thumbnail
    template_image_path = db.Column(db.String(200), nullable=True)
    thumbnail_path = db.Column(db.String(200), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'region1': {
                'width': self.region1_width,
                'height': self.region1_height,
                'x': self.region1_x,
                'y': self.region1_y
            },
            'region2': {
                'width': self.region2_width,
                'height': self.region2_height,
                'x': self.region2_x,
                'y': self.region2_y
            },
            'template_image_path': self.template_image_path,
            'thumbnail_path': self.thumbnail_path
        }
    
    def to_csv(self):
        return f"region,width,height,x,y\n" \
               f"region1,{self.region1_width},{self.region1_height},{self.region1_x},{self.region1_y}\n" \
               f"region2,{self.region2_width},{self.region2_height},{self.region2_x},{self.region2_y}"
