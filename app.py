from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
from models import db, User, Account, Transaction, AuditLog, SecurityEvent
from models import AccountType, AccountStatus, TransactionType, TransactionStatus, UserRole
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime, timedelta
from functools import wraps
import pyotp
import qrcode
import io
import base64
import secrets
import re
from decimal import Decimal
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
CORS(app, origins=app.config['CORS_ORIGINS'])
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)

# Password hasher
ph = PasswordHasher()

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
    
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('First National Bank startup')

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    for header, value in app.config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    return response

# Audit logging middleware
@app.before_request
def log_request():
    """Log all requests for audit trail"""
    g.request_start_time = datetime.utcnow()
    
@app.after_request
def log_response(response):
    """Log response and create audit trail"""
    if request.endpoint not in ['static', 'health']:
        duration = (datetime.utcnow() - g.request_start_time).total_seconds()
        app.logger.info(f"{request.method} {request.path} {response.status_code} {duration:.3f}s")
    return response

# JWT helper functions
def generate_jwt(user_id, token_type='access'):
    """Generate JWT token"""
    expiry = app.config['JWT_ACCESS_TOKEN_EXPIRES'] if token_type == 'access' else app.config['JWT_REFRESH_TOKEN_EXPIRES']
    payload = {
        'user_id': user_id,
        'type': token_type,
        'exp': datetime.utcnow() + expiry,
        'iat': datetime.utcnow(),
        'jti': secrets.token_urlsafe(16)  # Unique token ID
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_jwt(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication decorator
def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        payload = verify_jwt(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = User.query.get(payload['user_id'])
        if not user or user.account_locked:
            return jsonify({'error': 'Account locked or not found'}), 403
        
        g.current_user = user
        
        # Log access
        audit_log = AuditLog(
            user_id=user.id,
            action=f.__name__,
            resource=request.endpoint,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            request_method=request.method,
            request_url=request.url,
            success=True
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return f(*args, **kwargs)
    return decorated

# Role-based access control decorator
def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            if g.current_user.role.value != role and g.current_user.role != UserRole.ADMIN:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator

# Input validation helpers
def validate_password(password):
    """Validate password strength"""
    if len(password) < app.config['PASSWORD_MIN_LENGTH']:
        return False, f"Password must be at least {app.config['PASSWORD_MIN_LENGTH']} characters"
    
    if app.config['PASSWORD_REQUIRE_UPPERCASE'] and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if app.config['PASSWORD_REQUIRE_LOWERCASE'] and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if app.config['PASSWORD_REQUIRE_DIGIT'] and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if app.config['PASSWORD_REQUIRE_SPECIAL'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return text
    # Remove potential XSS vectors
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    return text.strip()

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit(app.config['RATELIMIT_LOGIN'])
def register():
    """Register new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Sanitize inputs
    username = sanitize_input(data['username'])
    email = sanitize_input(data['email'])
    
    # Validate email
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password
    valid, message = validate_password(data['password'])
    if not valid:
        return jsonify({'error': message}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    from models import encrypt_data
    user = User(
        username=username,
        email=email,
        password_hash=ph.hash(data['password']),
        first_name=encrypt_data(sanitize_input(data['first_name'])),
        last_name=encrypt_data(sanitize_input(data['last_name'])),
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
        phone_number=encrypt_data(data.get('phone_number', '')),
        address=encrypt_data(data.get('address', ''))
    )
    
    db.session.add(user)
    db.session.commit()
    
    app.logger.info(f"New user registered: {username}")
    
    return jsonify({
        'message': 'Registration successful',
        'user_id': user.id
    }), 201

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit(app.config['RATELIMIT_LOGIN'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check if account is locked
    if user.account_locked:
        if user.last_failed_login and (datetime.utcnow() - user.last_failed_login) > app.config['ACCOUNT_LOCKOUT_DURATION']:
            user.account_locked = False
            user.failed_login_attempts = 0
            db.session.commit()
        else:
            return jsonify({'error': 'Account is locked. Try again later.'}), 403
    
    # Verify password
    try:
        ph.verify(user.password_hash, data['password'])
        
        # Reset failed attempts
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate tokens
        access_token = generate_jwt(user.id, 'access')
        refresh_token = generate_jwt(user.id, 'refresh')
        
        app.logger.info(f"User logged in: {user.username}")
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'mfa_enabled': user.mfa_enabled
            }
        }), 200
        
    except VerifyMismatchError:
        # Increment failed attempts
        user.failed_login_attempts += 1
        user.last_failed_login = datetime.utcnow()
        
        if user.failed_login_attempts >= app.config['MAX_LOGIN_ATTEMPTS']:
            user.account_locked = True
            
            # Log security event
            event = SecurityEvent(
                user_id=user.id,
                event_type='account_locked',
                severity='high',
                description=f'Account locked after {user.failed_login_attempts} failed login attempts',
                ip_address=request.remote_addr
            )
            db.session.add(event)
        
        db.session.commit()
        
        remaining = app.config['MAX_LOGIN_ATTEMPTS'] - user.failed_login_attempts
        return jsonify({
            'error': 'Invalid credentials',
            'attempts_remaining': max(0, remaining)
        }), 401

# ==================== ACCOUNT ENDPOINTS ====================

@app.route('/api/accounts', methods=['GET'])
@require_auth
@limiter.limit(app.config['RATELIMIT_API'])
def get_accounts():
    """Get all accounts for current user"""
    accounts = Account.query.filter_by(user_id=g.current_user.id).all()
    
    return jsonify({
        'accounts': [{
            'id': acc.id,
            'account_number': acc.get_masked_account_number(),
            'account_type': acc.account_type.value,
            'nickname': acc.nickname,
            'balance': acc.get_balance(),
            'status': acc.status.value,
            'opened_at': acc.opened_at.isoformat()
        } for acc in accounts]
    }), 200

@app.route('/api/accounts/<account_type>', methods=['POST'])
@require_auth
@limiter.limit(app.config['RATELIMIT_API'])
def create_account(account_type):
    """Create new account"""
    # Generate unique account number
    account_number = f"FNCA{secrets.randbelow(10**12):012d}"
    
    # Map account type to enum
    account_type_map = {
        'savings': AccountType.SAVINGS,
        'checking': AccountType.CHECKING,
        'cd': AccountType.CD,
        'moneymarket': AccountType.MONEY_MARKET,
        'mutualfund': AccountType.MUTUAL_FUND
    }
    
    if account_type not in account_type_map:
        return jsonify({'error': 'Invalid account type'}), 400
    
    from models import encrypt_data
    account = Account(
        user_id=g.current_user.id,
        account_number=encrypt_data(account_number),
        account_type=account_type_map[account_type],
        status=AccountStatus.ACTIVE
    )
    
    # Set interest rate based on type
    if account_type == 'savings':
        account.interest_rate = Decimal(str(app.config['SAVINGS_APY']))
    elif account_type == 'checking':
        account.interest_rate = Decimal(str(app.config['CHECKING_APY']))
    elif account_type == 'moneymarket':
        account.interest_rate = Decimal(str(app.config['MONEYMARKET_APY']))
    
    db.session.add(account)
    db.session.commit()
    
    app.logger.info(f"New account created: {account_type} for user {g.current_user.username}")
    
    return jsonify({
        'message': 'Account created successfully',
        'account_id': account.id,
        'account_number': account.get_masked_account_number()
    }), 201

@app.route('/api/balance', methods=['GET'])
@require_auth
@limiter.limit(app.config['RATELIMIT_API'])
def get_total_balance():
    """Get total cash balance across all accounts"""
    accounts = Account.query.filter_by(user_id=g.current_user.id, status=AccountStatus.ACTIVE).all()
    
    total_balance = sum(acc.get_balance() for acc in accounts)
    
    return jsonify({
        'total_balance': total_balance,
        'accounts': [{
            'id': acc.id,
            'type': acc.account_type.value,
            'balance': acc.get_balance()
        } for acc in accounts]
    }), 200

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# ==================== DATABASE INITIALIZATION ====================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
