from datetime import datetime
from flask import current_app
import json
from datetime import date, datetime

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    """Format a datetime object to a string."""
    if value is None:
        return ""
    try:
        return value.strftime(format)
    except Exception as e:
        current_app.logger.error(f'Error in datetimeformat: {str(e)}')
        return str(value)  # Trả về giá trị gốc nếu có lỗi

def tojson_filter(obj, **kwargs):
    """Convert a Python object to a JSON string, handling datetime objects."""
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    try:
        return json.dumps(obj, default=json_serial, **kwargs)
    except Exception as e:
        current_app.logger.error(f'Error in tojson filter: {str(e)}')
        return json.dumps({'error': str(e)})

def register_filters(app):
    """Register all filters with the Flask app."""
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['tojson'] = tojson_filter
    app.logger.info('Registered datetimeformat and tojson filters')
