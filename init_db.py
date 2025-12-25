#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Initialize database and create a default user
"""
import sys
from app import app, db
from app.models import User

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
            admin = User(
                user='admin',
                name='Administrator',
                email='admin@example.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("IMPORTANT: Please change the default password after first login!")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
