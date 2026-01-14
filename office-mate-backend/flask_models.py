"""
SQLAlchemy Models for Flask Application
Minimal, production-ready models for Office Mate system
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many-to-many association table for Document-Tag relationship
document_tags = db.Table(
    'document_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True, index=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True, index=True)
)


class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='owner', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Tag(db.Model):
    """Tag model for document categorization"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'


class Document(db.Model):
    """Document model with OCR and classification"""
    __tablename__ = 'documents'
    __table_args__ = (
        # Composite index for common query pattern (user + date range)
        db.Index('idx_user_created', 'user_id', 'created_at'),
        # Composite index for user + category filtering
        db.Index('idx_user_category', 'user_id', 'category'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(500), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, default='')
    category = db.Column(db.String(50), default='unknown', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Many-to-many relationship with tags
    tags = db.relationship('Tag', secondary=document_tags, lazy='subquery',
                          backref=db.backref('documents', lazy=True))
    
    # One-to-many relationship with tasks
    tasks = db.relationship('Task', backref='document', lazy=True)
    
    def __repr__(self):
        return f'<Document {self.original_name}>'


class Task(db.Model):
    """Task model for to-do management"""
    __tablename__ = 'tasks'
    __table_args__ = (
        # Composite index for user + status filtering
        db.Index('idx_task_user_status', 'user_id', 'status'),
        # Composite index for user + due date
        db.Index('idx_task_user_due', 'user_id', 'due_date'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    priority = db.Column(db.String(20), default='Low')  # Low, Medium, High, Urgent
    due_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(20), default='Todo', index=True)  # Todo, InProgress, Done
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'


# Helper function to initialize database
def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
