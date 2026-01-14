"""
Flask Application with Document Upload API
Complete app.py example integrating all components
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_models import db, init_db
from flask_documents_api import documents_bp
from flask_auth import auth_bp
from flask_tasks_api import tasks_bp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///office_mate.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 10 * 1024 * 1024))  # 10 MB default

# Get CORS origins from environment
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000,http://localhost:8081').split(',')

# Enable CORS for frontend
CORS(app, origins=cors_origins, supports_credentials=True)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(tasks_bp)

# Health check endpoint
@app.route('/')
def health_check():
    return {'status': 'ok', 'message': 'Office Mate API is running'}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
