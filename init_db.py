#!/usr/bin/env python3
"""
Database initialization script for Smart Management Hub
Run this script to create all database tables
"""

from app import app, db
from models import Business, Plan, Customer, Subscription, Payment

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        print("📊 Tables created:")
        print("   - businesses")
        print("   - plans") 
        print("   - customers")
        print("   - subscriptions")
        print("   - payments")
        print("\n🚀 Your Smart Management Hub is ready to use!")

if __name__ == "__main__":
    init_database() 