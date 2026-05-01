"""
Security Modules for First National Collegiate Bank

Provides:
- Universal university authentication (any .edu)
- Autonomous CVE monitoring
- Auto-patching system
- Security integration
"""

from .universal_edu_auth import (
    authenticate_student,
    UniversalEduAuth,
    University
)

from .autonomous_cve_monitor import (
    CVEMonitor,
    AutoPatcher,
    run_daily_security_scan,
    CVE
)

from .integration import (
    SecureBank,
    create_secure_flask_app,
    setup_daily_security_scan
)

__version__ = "1.0.0"
__all__ = [
    'authenticate_student',
    'UniversalEduAuth',
    'University',
    'CVEMonitor',
    'AutoPatcher',
    'run_daily_security_scan',
    'CVE',
    'SecureBank',
    'create_secure_flask_app',
    'setup_daily_security_scan'
]
