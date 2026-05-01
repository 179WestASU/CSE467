# Security Bolstering System

## Universal University Authentication
Generalized Duo-compatible 1FA for any higher education institution.

### Features
- ✅ Works with any .edu domain
- ✅ Auto-detects university from email
- ✅ 2-digit verification code (Duo-compatible)
- ✅ Supports ASU, MIT, Stanford, Harvard, and any university
- ✅ Secure JWT token generation
- ✅ Session management

### Usage
```python
from security_modules.universal_edu_auth import authenticate_student

# One-line authentication
success, user_data = authenticate_student(
    email="student@asu.edu",
    password="SecurePass123",
    duo_code="42"  # 2-digit verification
)

if success:
    print(f"Welcome {user_data['email']}")
    print(f"Token: {user_data['session_token']}")
```

## Autonomous CVE Monitoring

### Features
- ✅ Daily CVE scanning from multiple sources:
  - NVD (National Vulnerability Database)
  - Grafana Security Advisories
  - GitHub Security Advisories
  - Python Safety DB
- ✅ Automatic severity classification
- ✅ Auto-patching for critical/high severity
- ✅ Dependency tracking
- ✅ Daily security reports

### Usage
```python
from security_modules.autonomous_cve_monitor import run_daily_security_scan

# Run daily (add to cron/scheduler)
dependencies = [
    'Flask==3.0.3',
    'SQLAlchemy==2.0.30',
    'argon2-cffi==23.1.0'
]

cves, patches = await run_daily_security_scan(dependencies)
print(f"Found {len(cves)} CVEs, applied {patches['successful']} patches")
```

## Integration

Both systems are ready for production use. See integration examples in `/examples/`.
