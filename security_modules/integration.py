"""
Security Integration Module
Integrates universal auth and CVE monitoring with banking application
"""

from typing import Dict, Optional, List
from datetime import datetime
import asyncio
from .universal_edu_auth import authenticate_student, UniversalEduAuth, University
from .autonomous_cve_monitor import run_daily_security_scan, CVEMonitor
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SecureBank:
    """
    Enhanced banking application with:
    - Universal university authentication
    - Autonomous CVE monitoring
    - Auto-patching
    """
    
    def __init__(self, app_dependencies: List[str]):
        """
        Initialize secure banking system
        
        Args:
            app_dependencies: List of Python packages used by the app
        """
        self.dependencies = app_dependencies
        self.cve_monitor = CVEMonitor(app_dependencies)
        self.authenticated_users = {}
        
        logger.info("SecureBank initialized with autonomous security monitoring")
    
    async def login_student(
        self, 
        email: str, 
        password: str, 
        verification_code: str
    ) -> Dict:
        """
        Authenticate student using universal university auth
        
        Args:
            email: Student email (e.g., student@asu.edu)
            password: Student password
            verification_code: 2-digit Duo code
            
        Returns:
            Authentication result with user data
        """
        try:
            # Authenticate
            success, user_data = authenticate_student(email, password, verification_code)
            
            if success:
                # Store session
                self.authenticated_users[user_data['session_token']] = user_data
                
                logger.info(f"Student authenticated: {user_data['email']} from {user_data['university']}")
                
                return {
                    'success': True,
                    'user': user_data,
                    'message': f"Welcome to First National Bank, {user_data['email']}"
                }
            else:
                logger.warning(f"Authentication failed for {email}")
                return {
                    'success': False,
                    'error': 'Authentication failed. Please check credentials and verification code.'
                }
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return {
                'success': False,
                'error': 'An error occurred during authentication'
            }
    
    def verify_session(self, token: str) -> Optional[Dict]:
        """Verify active session token"""
        return self.authenticated_users.get(token)
    
    async def run_security_scan(self) -> Dict:
        """
        Run autonomous security scan
        Should be scheduled daily (e.g., via cron)
        """
        logger.info("Starting daily security scan...")
        
        try:
            cves, patch_results = await run_daily_security_scan(self.dependencies)
            
            result = {
                'scan_time': datetime.now().isoformat(),
                'cves_found': len(cves),
                'critical': sum(1 for c in cves if c.severity == 'CRITICAL'),
                'high': sum(1 for c in cves if c.severity == 'HIGH'),
                'medium': sum(1 for c in cves if c.severity == 'MEDIUM'),
                'low': sum(1 for c in cves if c.severity == 'LOW'),
                'patches_applied': patch_results['successful'] if patch_results else 0,
                'status': 'complete'
            }
            
            logger.info(f"Security scan complete: {result['cves_found']} CVEs found, {result['patches_applied']} patches applied")
            
            return result
            
        except Exception as e:
            logger.error(f"Security scan error: {e}")
            return {
                'scan_time': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }
    
    def get_security_status(self) -> Dict:
        """Get current security posture"""
        return {
            'last_scan': self.cve_monitor.last_scan.isoformat() if self.cve_monitor.last_scan else None,
            'monitored_packages': len(self.cve_monitor.dependencies),
            'known_vulnerabilities': len(self.cve_monitor.cve_database),
            'active_sessions': len(self.authenticated_users),
            'status': 'secure'
        }


# Flask Integration Example
def create_secure_flask_app():
    """
    Example: Integrate with Flask application
    """
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    # Initialize secure bank
    dependencies = [
        'Flask==3.0.3',
        'SQLAlchemy==2.0.30',
        'argon2-cffi==23.1.0',
        'PyJWT==2.8.0',
        'cryptography==42.0.7'
    ]
    
    secure_bank = SecureBank(dependencies)
    
    @app.route('/api/auth/login', methods=['POST'])
    async def login():
        """Student login endpoint"""
        data = request.json
        
        result = await secure_bank.login_student(
            email=data.get('email'),
            password=data.get('password'),
            verification_code=data.get('duo_code')
        )
        
        return jsonify(result)
    
    @app.route('/api/security/status', methods=['GET'])
    def security_status():
        """Security status endpoint"""
        return jsonify(secure_bank.get_security_status())
    
    @app.route('/api/security/scan', methods=['POST'])
    async def trigger_scan():
        """Manually trigger security scan"""
        result = await secure_bank.run_security_scan()
        return jsonify(result)
    
    return app


# Scheduler Setup for Daily Scans
def setup_daily_security_scan(dependencies: List[str]):
    """
    Setup daily automated security scanning
    Can be run as cron job or with APScheduler
    """
    import schedule
    import time
    
    async def scan_task():
        """Daily scan task"""
        logger.info("Running scheduled security scan...")
        await run_daily_security_scan(dependencies)
    
    # Schedule daily at 2 AM
    schedule.every().day.at("02:00").do(lambda: asyncio.run(scan_task()))
    
    logger.info("Daily security scan scheduled for 02:00")
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("Secure Banking System - Integration Test")
    print("=" * 60)
    
    # Initialize
    deps = ['Flask==3.0.3', 'SQLAlchemy==2.0.30']
    bank = SecureBank(deps)
    
    # Test authentication
    async def test():
        result = await bank.login_student(
            "student@asu.edu",
            "TestPass123",
            "42"
        )
        print(f"\nAuthentication: {result['success']}")
        
        # Test security scan
        scan_result = await bank.run_security_scan()
        print(f"\nSecurity Scan: {scan_result['status']}")
        print(f"CVEs Found: {scan_result.get('cves_found', 0)}")
        print(f"Patches Applied: {scan_result.get('patches_applied', 0)}")
        
        # Get status
        status = bank.get_security_status()
        print(f"\nSecurity Status:")
        print(f"  Monitored Packages: {status['monitored_packages']}")
        print(f"  Known Vulnerabilities: {status['known_vulnerabilities']}")
        print(f"  Active Sessions: {status['active_sessions']}")
    
    asyncio.run(test())
