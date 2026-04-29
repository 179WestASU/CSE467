# First National Collegiate Bank of AZ 🏦

## Mission Statement
A secure, accessible banking platform built by neurodivergent college students to empower everyone on their journey to financial literacy. We believe banking should be inclusive, educational, and secure.

## 🎯 Features

### Account Types
- **Savings Account** - High-yield savings with competitive APY
- **Checking Account** - Day-to-day transaction account with debit card access
- **Certificate of Deposit (CD)** - Fixed-term, higher-interest investment
- **Money Market Account** - Higher interest with limited transactions
- **Mutual Fund Deposit** - Investment account for mutual funds
- **Cash Balance Tracking** - Real-time balance monitoring across all accounts

### Security Features (CVE-Compliant as of April 26, 2024)

#### Authentication & Authorization
- ✅ **Argon2id password hashing** - Industry-leading password security
- ✅ **JWT with RS256** - Asymmetric token signing
- ✅ **Multi-factor authentication (MFA)** - TOTP-based 2FA
- ✅ **Account lockout** - Automatic lockout after 5 failed attempts
- ✅ **Session management** - Secure, httpOnly cookies
- ✅ **Role-based access control (RBAC)** - Customer, teller, admin roles

#### Data Protection
- ✅ **AES-256 encryption at rest** - All sensitive data encrypted
- ✅ **TLS 1.3** - Encrypted data in transit
- ✅ **Sensitive data masking** - Account numbers, SSN displayed partially
- ✅ **PCI-DSS compliance** - Secure card data handling
- ✅ **Database encryption** - SQLCipher for encrypted SQLite

#### Application Security
- ✅ **SQL Injection prevention** - Parameterized queries (CVE-2024-XXXX)
- ✅ **XSS protection** - Content Security Policy, input sanitization
- ✅ **CSRF protection** - Double-submit cookie pattern
- ✅ **Rate limiting** - Prevents brute force and DDoS
- ✅ **Input validation** - Comprehensive server-side validation
- ✅ **Secure headers** - HSTS, X-Frame-Options, CSP
- ✅ **API security** - Request signing, nonce validation
- ✅ **File upload validation** - Type checking, size limits, virus scanning

#### Monitoring & Compliance
- ✅ **Audit logging** - All transactions and access logged
- ✅ **Anomaly detection** - Unusual transaction patterns flagged
- ✅ **SIEM integration ready** - Structured logging for Grafana/ELK
- ✅ **PII protection** - GDPR/CCPA compliant data handling
- ✅ **Automatic security updates** - Dependency vulnerability scanning
- ✅ **Incident response** - Automated alerting and logging

#### Recent CVE Mitigations
- **Grafana CVE-2024-XXXX** - No direct dependencies, API secured
- **SQL Injection** - All queries parameterized
- **Authentication Bypass** - Strict JWT validation with expiry
- **Path Traversal** - Whitelist-based file access
- **SSRF Prevention** - URL validation, internal IP blocking
- **XML External Entity (XXE)** - XML parsing disabled
- **Deserialization** - Safe JSON parsing only

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10+
pip install -r requirements.txt
```

### Installation
```bash
# Clone repository
git clone https://github.com/179WestASU/CSE467.git
cd CSE467

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run application
python app.py
```

### Default Admin Credentials (CHANGE IMMEDIATELY)
```
Username: admin
Password: FirstBank2024!
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new customer
- `POST /api/auth/login` - Login with username/password
- `POST /api/auth/logout` - Logout and invalidate token
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/2fa/enable` - Enable 2FA
- `POST /api/auth/2fa/verify` - Verify 2FA code

### Account Endpoints
- `GET /api/accounts` - List all user accounts
- `GET /api/accounts/:id` - Get account details
- `POST /api/accounts/savings` - Create savings account
- `POST /api/accounts/checking` - Create checking account
- `POST /api/accounts/cd` - Create CD account
- `POST /api/accounts/moneymarket` - Create money market account
- `POST /api/accounts/mutualfund` - Create mutual fund account

### Transaction Endpoints
- `POST /api/transactions/deposit` - Deposit funds
- `POST /api/transactions/withdraw` - Withdraw funds
- `POST /api/transactions/transfer` - Transfer between accounts
- `GET /api/transactions/history` - Get transaction history
- `GET /api/balance` - Get real-time cash balance

### Security Endpoints
- `GET /api/security/audit-log` - View audit log (admin only)
- `POST /api/security/report` - Report suspicious activity
- `GET /api/security/status` - Check account security status

## 🔒 Security Best Practices

### For Developers
1. Never commit secrets to version control
2. Use environment variables for configuration
3. Keep dependencies updated
4. Run security scans regularly
5. Follow principle of least privilege
6. Implement defense in depth

### For Users
1. Enable 2FA immediately
2. Use strong, unique passwords
3. Monitor account activity regularly
4. Report suspicious activity
5. Never share credentials
6. Use secure networks only

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Load Balancer (NGINX)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  Web Server 1   │    │  Web Server 2   │
│  (Flask/Gunicorn)│    │  (Flask/Gunicorn)│
└────────┬────────┘    └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Application Layer    │
         │  - Authentication      │
         │  - Business Logic      │
         │  - Rate Limiting       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    Database Layer      │
         │  - PostgreSQL          │
         │  - Redis Cache         │
         │  - Encrypted Storage   │
         └────────────────────────┘
```

## 📊 Database Schema

### Users Table
- id (PK, UUID)
- username (unique, indexed)
- email (unique, indexed)
- password_hash (Argon2id)
- mfa_secret (encrypted)
- mfa_enabled (boolean)
- account_locked (boolean)
- failed_login_attempts (int)
- last_login (timestamp)
- created_at (timestamp)

### Accounts Table
- id (PK, UUID)
- user_id (FK to Users)
- account_number (unique, encrypted)
- account_type (enum)
- balance (decimal, encrypted)
- interest_rate (decimal)
- status (enum: active, frozen, closed)
- created_at (timestamp)

### Transactions Table
- id (PK, UUID)
- from_account_id (FK)
- to_account_id (FK)
- amount (decimal, encrypted)
- transaction_type (enum)
- status (enum)
- description (text)
- ip_address (inet)
- user_agent (text)
- created_at (timestamp)

### Audit Log Table
- id (PK, UUID)
- user_id (FK)
- action (text)
- resource (text)
- ip_address (inet)
- success (boolean)
- details (jsonb, encrypted)
- timestamp (timestamp)

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run security tests
pytest tests/security/

# Run load tests
locust -f tests/load/locustfile.py
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

We welcome contributions from the neurodiverse community! Please read CONTRIBUTING.md for guidelines.

## 🆘 Support

- **Documentation**: https://docs.firstnationalaz.bank
- **Email**: support@firstnationalaz.bank
- **Security Issues**: security@firstnationalaz.bank (PGP key available)

## 🏆 Accessibility Features

- **Screen reader compatible** - WCAG 2.1 AA compliant
- **Keyboard navigation** - Full keyboard accessibility
- **High contrast mode** - For visual impairments
- **Text-to-speech** - Built-in TTS for transactions
- **Simplified mode** - Reduced cognitive load interface
- **Clear language** - Plain language financial terms

---

**Built with 💙 by neurodivergent students, for everyone.**
