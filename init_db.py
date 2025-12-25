#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Initialize database and create a default user
"""
import sys
import secrets
import string
from app import app, db
from app.models import User

def generate_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def init_db():
    """Initialize the database and create tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(user='admin').first()
        if not admin:
            print("Creating default admin user...")
            # Generate a secure random password
            admin_password = generate_password()
            
            admin = User(
                user='admin',
                name='Administrator',
                email='admin@example.com'
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created successfully!")
            print("=" * 60)
            print("Username: admin")
            print(f"Password: {admin_password}")
            print("=" * 60)
            print("IMPORTANT: Save this password securely!")
            print("          This password will not be shown again.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
