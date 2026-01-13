"""
Database initialization and seeding script
Creates tables and optionally seeds initial data
"""
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models
from app.services.auth import get_password_hash


def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_default_tags(db: Session):
    """Seed default tags"""
    default_tags = [
        {"name": "Finance", "name_si": "මුල්‍ය", "color": "#10B981"},
        {"name": "HR", "name_si": "මානව සම්පත්", "color": "#F59E0B"},
        {"name": "Procurement", "name_si": "ප්‍රසම්පාදන", "color": "#3B82F6"},
        {"name": "Maintenance", "name_si": "නඩත්තුව", "color": "#EF4444"},
        {"name": "Invoice", "name_si": "ප්‍රේෂණ නිරීක්ෂණය", "color": "#8B5CF6"},
        {"name": "Contract", "name_si": "කොන්ත්‍රාත්තුව", "color": "#EC4899"},
        {"name": "Report", "name_si": "වාර්තාව", "color": "#14B8A6"},
        {"name": "Letter", "name_si": "ලිපිය", "color": "#6366F1"},
    ]
    
    for tag_data in default_tags:
        existing = db.query(models.Tag).filter(models.Tag.name == tag_data["name"]).first()
        if not existing:
            tag = models.Tag(**tag_data)
            db.add(tag)
    
    db.commit()
    print("Default tags seeded successfully!")


def create_admin_user(db: Session, username: str = "admin", password: str = "admin123", email: str = "admin@officemate.lk"):
    """Create an admin user"""
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        print(f"Admin user '{username}' already exists!")
        return existing_user
    
    user = models.User(
        username=username,
        email=email,
        full_name="System Administrator",
        hashed_password=get_password_hash(password),
        is_admin=True,
        is_active=True,
        preferred_language="en"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Admin user created: {username} / {password}")
    return user


def seed_data():
    """Seed initial data"""
    db = SessionLocal()
    try:
        print("\n=== Seeding database ===")
        seed_default_tags(db)
        create_admin_user(db)
        print("=== Database seeding completed ===\n")
    finally:
        db.close()


if __name__ == "__main__":
    print("\n=== Office Mate Database Initialization ===\n")
    init_db()
    
    seed = input("Do you want to seed initial data? (y/n): ")
    if seed.lower() == 'y':
        seed_data()
    
    print("\n=== Initialization completed ===\n")
