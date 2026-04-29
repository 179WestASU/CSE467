from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import uuid
from cryptography.fernet import Fernet
import os

db = SQLAlchemy()

# Encryption setup
encryption_key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(encryption_key)

def encrypt_data(data):
    """Encrypt sensitive data"""
    if data is None:
        return None
    return cipher_suite.encrypt(str(data).encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypt sensitive data"""
    if encrypted_data is None:
        return None
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

class AccountType(Enum):
    """Account types enumeration"""
    SAVINGS = 'savings'
    CHECKING = 'checking'
    CD = 'certificate_of_deposit'
    MONEY_MARKET = 'money_market'
    MUTUAL_FUND = 'mutual_fund'

class AccountStatus(Enum):
    """Account status enumeration"""
    ACTIVE = 'active'
    FROZEN = 'frozen'
    CLOSED = 'closed'
    PENDING = 'pending'

class TransactionType(Enum):
    """Transaction types"""
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    INTEREST = 'interest_payment'
    FEE = 'fee'
    REFUND = 'refund'

class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REVERSED = 'reversed'

class UserRole(Enum):
    """User roles for RBAC"""
    CUSTOMER = 'customer'
    TELLER = 'teller'
    MANAGER = 'manager'
    ADMIN = 'admin'

class User(db.Model):
    """User model with secure authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)  # Argon2id hash
    
    # Personal Information (encrypted)
    first_name = db.Column(db.String(255), nullable=False)  # Encrypted
    last_name = db.Column(db.String(255), nullable=False)  # Encrypted
    ssn_encrypted = db.Column(db.String(255))  # Encrypted SSN
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(255))  # Encrypted
    address = db.Column(db.Text)  # Encrypted
    
    # Security
    mfa_secret = db.Column(db.String(255))  # Encrypted TOTP secret
    mfa_enabled = db.Column(db.Boolean, default=False)
    account_locked = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Role
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('Account', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_full_name(self):
        """Get decrypted full name"""
        first = decrypt_data(self.first_name)
        last = decrypt_data(self.last_name)
        return f"{first} {last}"

class Account(db.Model):
    """Account model supporting multiple account types"""
    __tablename__ = 'accounts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Account Information
    account_number = db.Column(db.String(255), unique=True, nullable=False, index=True)  # Encrypted
    routing_number = db.Column(db.String(9), default='322271627')  # AZ routing number
    account_type = db.Column(db.Enum(AccountType), nullable=False, index=True)
    nickname = db.Column(db.String(100))  # User-friendly name
    
    # Financial Data (encrypted)
    balance_encrypted = db.Column(db.String(255), nullable=False, default=encrypt_data('0.00'))
    available_balance_encrypted = db.Column(db.String(255), nullable=False, default=encrypt_data('0.00'))
    
    # Account Specific Details
    interest_rate = db.Column(db.Numeric(5, 4), default=0.0000)  # APY as decimal
    minimum_balance = db.Column(db.Numeric(10, 2), default=0.00)
    cd_term_months = db.Column(db.Integer)  # For CD accounts
    cd_maturity_date = db.Column(db.Date)  # For CD accounts
    
    # Status
    status = db.Column(db.Enum(AccountStatus), default=AccountStatus.PENDING, nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    
    # Timestamps
    opened_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    closed_at = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions_from = db.relationship('Transaction',
                                       foreign_keys='Transaction.from_account_id',
                                       backref='from_account',
                                       lazy='dynamic')
    transactions_to = db.relationship('Transaction',
                                     foreign_keys='Transaction.to_account_id',
                                     backref='to_account',
                                     lazy='dynamic')
    
    def __repr__(self):
        return f'<Account {self.account_number[-4:]} - {self.account_type.value}>'
    
    def get_balance(self):
        """Get decrypted balance"""
        return float(decrypt_data(self.balance_encrypted))
    
    def set_balance(self, amount):
        """Set encrypted balance"""
        self.balance_encrypted = encrypt_data(f"{amount:.2f}")
    
    def get_masked_account_number(self):
        """Return masked account number (XXXX-XXXX-1234)"""
        decrypted = decrypt_data(self.account_number)
        return f"XXXX-XXXX-{decrypted[-4:]}"

class Transaction(db.Model):
    """Transaction model with full audit trail"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Transaction Details
    from_account_id = db.Column(db.String(36), db.ForeignKey('accounts.id'), index=True)
    to_account_id = db.Column(db.String(36), db.ForeignKey('accounts.id'), index=True)
    
    amount_encrypted = db.Column(db.String(255), nullable=False)  # Encrypted amount
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, index=True)
    status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    
    # Description and Reference
    description = db.Column(db.Text)
    reference_number = db.Column(db.String(50), unique=True, index=True)
    external_reference = db.Column(db.String(100))  # For external transactions
    
    # Security & Audit
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.Text)
    initiated_by_user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = db.Column(db.DateTime)
    
    # Fraud Detection Flags
    flagged_suspicious = db.Column(db.Boolean, default=False)
    risk_score = db.Column(db.Integer, default=0)  # 0-100
    
    def __repr__(self):
        return f'<Transaction {self.reference_number} - {self.transaction_type.value}>'
    
    def get_amount(self):
        """Get decrypted amount"""
        return float(decrypt_data(self.amount_encrypted))
    
    def set_amount(self, amount):
        """Set encrypted amount"""
        self.amount_encrypted = encrypt_data(f"{amount:.2f}")

class AuditLog(db.Model):
    """Comprehensive audit log for compliance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), index=True)
    
    # Action Details
    action = db.Column(db.String(100), nullable=False, index=True)
    resource = db.Column(db.String(100), index=True)
    resource_id = db.Column(db.String(36))
    
    # Request Details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    request_method = db.Column(db.String(10))
    request_url = db.Column(db.Text)
    
    # Result
    success = db.Column(db.Boolean, default=True, nullable=False)
    error_message = db.Column(db.Text)
    
    # Additional Context (encrypted JSON)
    details_encrypted = db.Column(db.Text)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} - {self.timestamp}>'

class SecurityEvent(db.Model):
    """Security events and anomalies"""
    __tablename__ = 'security_events'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), index=True)
    
    # Event Details
    event_type = db.Column(db.String(50), nullable=False, index=True)
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    description = db.Column(db.Text)
    
    # Context
    ip_address = db.Column(db.String(45))
    location = db.Column(db.String(100))
    
    # Status
    acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    acknowledged_at = db.Column(db.DateTime)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<SecurityEvent {self.event_type} - {self.severity}>'
