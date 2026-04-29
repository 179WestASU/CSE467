# Security Documentation
## First National Collegiate Bank of AZ

Last Updated: April 29, 2026

## 🔒 Security Architecture

### Defense in Depth

Our security model implements multiple layers of protection:

1. **Network Layer** - TLS 1.3, HTTPS enforcement
2. **Application Layer** - Input validation, CSRF protection, XSS prevention
3. **Authentication Layer** - Argon2id, JWT, MFA
4. **Authorization Layer** - RBAC, resource-level permissions
5. **Data Layer** - AES-256 encryption at rest, encrypted fields
6. **Monitoring Layer** - Audit logs, anomaly detection, SIEM integration

## 🛡️ CVE Mitigations (as of April 26, 2024)

### Critical CVEs Addressed

#### SQL Injection (CWE-89)
**Mitigation:**
- All database queries use SQLAlchemy ORM with parameterized queries
- No raw SQL execution without parameter binding
- Input validation on all user inputs
- Database user has minimum required permissions

```python
# SECURE - Parameterized query
user = User.query.filter_by(username=username).first()

# NEVER - String concatenation (vulnerable)
# query = f"SELECT * FROM users WHERE username='{username}'"
```

#### Cross-Site Scripting (XSS) - CVE-2024-XXXX
**Mitigation:**
- Content Security Policy (CSP) headers
- Input sanitization on all user-provided data
- Output encoding
- HTTPOnly and Secure cookie flags
- No inline JavaScript execution

#### Cross-Site Request Forgery (CSRF)
**Mitigation:**
- CSRF tokens on all state-changing operations
- SameSite cookie attribute
- Origin header validation
- Double-submit cookie pattern

#### Authentication Bypass
**Mitigation:**
- Argon2id password hashing (memory-hard, GPU-resistant)
- JWT with RS256 (asymmetric signing)
- Token expiry and rotation
- Account lockout after failed attempts
- MFA support (TOTP)

#### Session Management
**Mitigation:**
- Secure, HTTPOnly, SameSite cookies
- Session timeout after inactivity
- Logout invalidates tokens
- No session fixation vulnerabilities

#### Path Traversal (CVE-2024-XXXX)
**Mitigation:**
- Whitelist-based file access
- No direct file path manipulation from user input
- Sandboxed upload directory
- File type validation

#### Server-Side Request Forgery (SSRF)
**Mitigation:**
- URL validation
- Blacklist of internal IP ranges
- No arbitrary URL fetching from user input
- Timeout on external requests

#### XML External Entity (XXE)
**Mitigation:**
- XML parsing disabled
- JSON-only API
- No external entity resolution

#### Insecure Deserialization
**Mitigation:**
- JSON parsing only (no pickle, marshal, etc.)
- Input validation before deserialization
- Type checking

#### Weak Cryptography
**Mitigation:**
- AES-256 for encryption at rest
- TLS 1.3 for data in transit
- Argon2id for password hashing
- RS256 for JWT signing
- Secure random generation (secrets module)

#### Insufficient Logging & Monitoring
**Mitigation:**
- Comprehensive audit logging
- Security event logging
- Failed authentication tracking
- Anomaly detection
- Log rotation and retention

### Grafana-Specific CVEs (April 2024)

**CVE-2024-XXXX (Grafana Authentication Bypass)**
- We don't use Grafana directly in the application
- If deploying Grafana for monitoring:
  - Use latest patched version
  - Separate authentication
  - Network isolation
  - Read-only access for monitoring

## 🔐 Authentication & Authorization

### Password Requirements
- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character
- Not in common password list
- Argon2id hashing (memory-hard)

### Multi-Factor Authentication (MFA)
- TOTP-based (Time-based One-Time Password)
- Compatible with Google Authenticator, Authy
- Backup codes provided
- Mandatory for admin accounts

### JWT Tokens
- RS256 asymmetric signing
- 15-minute access token expiry
- 30-day refresh token expiry
- JTI (JWT ID) for revocation
- Stored in HTTPOnly cookies

### Role-Based Access Control (RBAC)
- **Customer** - Own accounts only
- **Teller** - Customer account access
- **Manager** - Branch-level access
- **Admin** - Full system access

## 🔒 Data Protection

### Encryption at Rest
- AES-256 encryption for sensitive fields:
  - Account numbers
  - SSN
  - Transaction amounts
  - Personal information
- Database-level encryption (SQLCipher)
- Encrypted backups

### Encryption in Transit
- TLS 1.3 required
- HSTS header enforced
- No mixed content
- Certificate pinning recommended

### PII Protection
- GDPR compliant
- CCPA compliant
- Right to be forgotten
- Data minimization
- Consent management

## 🚨 Incident Response

### Security Event Detection
1. Failed login attempts
2. Account lockouts
3. Suspicious transactions
4. Rate limit violations
5. Permission violations
6. SQL injection attempts
7. XSS attempts

### Alert Thresholds
- **Low** - Single failed login
- **Medium** - 3 failed logins in 5 minutes
- **High** - 5 failed logins (account lockout)
- **Critical** - SQL injection attempt detected

### Response Procedures
1. **Detection** - Security event logged
2. **Analysis** - Automated risk scoring
3. **Containment** - Account lockout, IP ban
4. **Investigation** - Audit log review
5. **Remediation** - Fix vulnerability
6. **Post-mortem** - Update security controls

## 📊 Compliance

### Standards & Regulations
- **PCI-DSS** - Payment card industry standards
- **GLBA** - Gramm-Leach-Bliley Act
- **GDPR** - General Data Protection Regulation
- **CCPA** - California Consumer Privacy Act
- **SOC 2 Type II** - Security, availability, confidentiality

### Audit Requirements
- Transaction logs: 7 years retention
- Access logs: 2 years retention
- Security events: 1 year retention
- Encrypted backups: Daily
- Disaster recovery: RTO 4 hours, RPO 1 hour

## 🔍 Penetration Testing

### Testing Schedule
- **External** - Quarterly
- **Internal** - Semi-annually
- **Code Review** - Every release
- **Dependency Scan** - Daily (automated)

### Testing Scope
- Authentication bypass
- Authorization bypass
- SQL injection
- XSS
- CSRF
- Business logic flaws
- Rate limiting
- Session management

## 📝 Security Checklist

### Pre-Production
- [ ] All default passwords changed
- [ ] Environment variables configured
- [ ] HTTPS/TLS enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Backups configured
- [ ] Monitoring configured
- [ ] Dependency vulnerability scan passed
- [ ] Penetration test completed

### Production Monitoring
- [ ] Failed login monitoring
- [ ] Transaction anomaly detection
- [ ] Database performance monitoring
- [ ] API rate limit monitoring
- [ ] Error rate monitoring
- [ ] Security event alerts

## 🆘 Security Contacts

- **Security Team**: security@firstnationalaz.bank
- **Bug Bounty**: bugbounty@firstnationalaz.bank
- **Incident Response**: incidents@firstnationalaz.bank
- **PGP Key**: https://firstnationalaz.bank/security/pgp

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PCI-DSS Requirements](https://www.pcisecuritystandards.org/)

---

**Report security vulnerabilities responsibly. We have a bug bounty program.**
