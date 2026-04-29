#!/usr/bin/env python3
"""
Database initialization script for First National Collegiate Bank of AZ
Creates tables and seeds initial data
"""

from app import app, db
from models import User, Account, AccountType, AccountStatus, UserRole
from models import encrypt_data
from argon2 import PasswordHasher
from datetime import datetime, date
import secrets

ph = PasswordHasher()

def init_database():
    """Initialize database with tables and seed data"""
    print("🏦 Initializing First National Collegiate Bank database...")
    
    with app.app_context():
        # Drop all tables (WARNING: This deletes all data)
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@firstnationalaz.bank',
            password_hash=ph.hash('FirstBank2024!'),
            first_name=encrypt_data('System'),
            last_name=encrypt_data('Administrator'),
            date_of_birth=date(1990, 1, 1),
            phone_number=encrypt_data('555-0100'),
            role=UserRole.ADMIN,
            mfa_enabled=False
        )
        db.session.add(admin)
        
        # Create sample customer
        print("Creating sample customer...")
        customer = User(
            username='demo_user',
            email='demo@example.com',
            password_hash=ph.hash('Demo123!@#'),
            first_name=encrypt_data('Demo'),
            last_name=encrypt_data('User'),
            date_of_birth=date(1995, 6, 15),
            phone_number=encrypt_data('555-0123'),
            address=encrypt_data('123 Main St, Phoenix, AZ 85001'),
            role=UserRole.CUSTOMER
        )
        db.session.add(customer)
        db.session.commit()
        
        # Create sample accounts for demo user
        print("Creating sample accounts...")
        
        # Savings Account
        savings_account_number = f"FNCA{secrets.randbelow(10**12):012d}"
        savings = Account(
            user_id=customer.id,
            account_number=encrypt_data(savings_account_number),
            account_type=AccountType.SAVINGS,
            nickname='Emergency Fund',
            status=AccountStatus.ACTIVE,
            interest_rate=0.0425,  # 4.25% APY
            is_primary=True
        )
        savings.set_balance(5000.00)
        db.session.add(savings)
        
        # Checking Account
        checking_account_number = f"FNCA{secrets.randbelow(10**12):012d}"
        checking = Account(
            user_id=customer.id,
            account_number=encrypt_data(checking_account_number),
            account_type=AccountType.CHECKING,
            nickname='Primary Checking',
            status=AccountStatus.ACTIVE,
            interest_rate=0.0001
        )
        checking.set_balance(1500.00)
        db.session.add(checking)
        
        # CD Account
        cd_account_number = f"FNCA{secrets.randbelow(10**12):012d}"
        cd = Account(
            user_id=customer.id,
            account_number=encrypt_data(cd_account_number),
            account_type=AccountType.CD,
            nickname='12-Month CD',
            status=AccountStatus.ACTIVE,
            interest_rate=0.0525,  # 5.25% APY
            cd_term_months=12
        )
        cd.set_balance(10000.00)
        db.session.add(cd)
        
        db.session.commit()
        
        print("\n✅ Database initialized successfully!")
        print("\n📊 Summary:")
        print(f"   Users created: {User.query.count()}")
        print(f"   Accounts created: {Account.query.count()}")
        print("\n🔑 Login Credentials:")
        print("   Admin:")
        print("     Username: admin")
        print("     Password: FirstBank2024!")
        print("\n   Demo Customer:")
        print("     Username: demo_user")
        print("     Password: Demo123!@#")
        print("\n⚠️  IMPORTANT: Change default passwords immediately in production!")

if __name__ == '__main__':
    init_database()
