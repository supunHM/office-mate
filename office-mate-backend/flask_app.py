"""
Flask Application with Document Upload API
Complete app.py example integrating all components
"""
from flask import Flask
from flask_cors import CORS
from flask_models import db, init_db
from flask_documents_api import documents_bp
from flask_auth import auth_bp
from flask_tasks_api import tasks_bp

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max file size

# Enable CORS for frontend
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

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
    app.run(debug=True, host='0.0.0.0', port=5001)
