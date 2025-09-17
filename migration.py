# migration.py
from app import app, db
from models import User

with app.app_context():
    # Add new columns if they don't exist
    try:
        # This is a simple approach - in production use proper migrations like Flask-Migrate
        db.engine.execute('ALTER TABLE user ADD COLUMN theme_preference VARCHAR(20) DEFAULT "system"')
        db.engine.execute('ALTER TABLE user ADD COLUMN email_notifications BOOLEAN DEFAULT TRUE')
        db.engine.execute('ALTER TABLE user ADD COLUMN auto_save BOOLEAN DEFAULT TRUE')
        db.engine.execute('ALTER TABLE user ADD COLUMN summary_length INTEGER DEFAULT 150')
        db.engine.execute('ALTER TABLE user ADD COLUMN items_per_page INTEGER DEFAULT 10')
        print("✅ Database schema updated successfully!")
    except Exception as e:
        print(f"⚠️  Database may already have these columns: {e}")