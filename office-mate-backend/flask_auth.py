"""
Flask Authentication API
POST /api/auth/register - Register new user
POST /api/auth/login - Login and get JWT token
GET /api/auth/me - Get current user info
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from functools import wraps

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Secret key for JWT (should be in environment variable in production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


def create_access_token(user_id: int, username: str) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        # Verify token
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user from database
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # Pass user to the route function
        return f(current_user=user, *args, **kwargs)
    
    return decorated


def get_current_user():
    """
    Helper function to get current user ID from request headers
    Returns user_id if authenticated, None otherwise
    Used by document and task endpoints
    """
    token = None
    
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            # Format: "Bearer <token>"
            token = auth_header.split(' ')[1]
        except IndexError:
            return None
    
    if not token:
        return None
    
    # Verify token
    payload = verify_token(token)
    if not payload:
        return None
    
    return payload.get('user_id')


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register a new user
    Request Body:
    {
      "username": "string",
      "email": "user@example.com",
      "password": "string",
      "full_name": "string (optional)",
      "preferred_language": "en" (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        preferred_language = data.get('preferred_language', 'en')
        
        # Validation
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name if full_name else None
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(new_user.id, new_user.username)
        
        # Return user data
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'full_name': new_user.full_name,
                'created_at': new_user.created_at.isoformat()
            },
            'access_token': access_token,
            'token_type': 'bearer'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login user
    Accepts both JSON and form-data
    JSON Body:
    {
      "username": "string",
      "password": "string"
    }
    OR Form Data:
    - username: string
    - password: string
    """
    try:
        # Accept both JSON and form-data
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
        else:
            # Form data
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
        
        # Validation
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Create access token
        access_token = create_access_token(user.id, user.username)
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name
            },
            'access_token': access_token,
            'token_type': 'bearer'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user_info(current_user):
    """
    Get current user info
    Requires: Authorization header with Bearer token
    """
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'created_at': current_user.created_at.isoformat()
    }), 200


@auth_bp.route('/api/auth/me', methods=['PUT'])
@token_required
def update_current_user(current_user):
    """
    Update current user info
    Requires: Authorization header with Bearer token
    Request Body (all optional):
    {
      "email": "newemail@example.com",
      "full_name": "New Name",
      "password": "newpassword"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Update email if provided
        if 'email' in data:
            email = data['email'].strip()
            if email:
                # Check if email already exists for another user
                existing = User.query.filter_by(email=email).first()
                if existing and existing.id != current_user.id:
                    return jsonify({'error': 'Email already exists'}), 400
                current_user.email = email
        
        # Update full name if provided
        if 'full_name' in data:
            current_user.full_name = data['full_name'].strip()
        
        # Update password if provided
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            current_user.password_hash = generate_password_hash(password)
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'full_name': current_user.full_name,
                'created_at': current_user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500


@auth_bp.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Logout user (client-side token removal)
    Requires: Authorization header with Bearer token
    """
    return jsonify({
        'message': 'Logout successful. Please remove the token from client storage.'
    }), 200


# Test endpoint (unprotected)
@auth_bp.route('/api/auth/test', methods=['GET'])
def test_auth():
    """Test if auth endpoints are working"""
    return jsonify({
        'status': 'ok',
        'message': 'Authentication API is running',
        'endpoints': [
            'POST /api/auth/register',
            'POST /api/auth/login',
            'GET /api/auth/me (protected)',
            'PUT /api/auth/me (protected)',
            'POST /api/auth/logout (protected)'
        ]
    }), 200
