""
WSGI config for Image Processor.

This module contains the WSGI application used by the production server.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the default configuration
os.environ.setdefault('FLASK_ENV', 'production')

# Create application
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    # This is used when running the application directly
    # Useful for development
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    app.run(host=host, port=port, debug=debug)
