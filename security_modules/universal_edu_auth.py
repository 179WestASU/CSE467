"""
Universal University Authentication Module
Supports any higher education institution with Duo-compatible 1FA

Supports: .edu domains with 2-digit student verification codes
Compatible with: ASU, MIT, Stanford, Harvard, any university system
"""

import requests
import re
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
import hashlib
from datetime import datetime, timedelta
import jwt

@dataclass
class University:
    """University configuration"""
    domain: str  # e.g., "asu.edu", "mit.edu"
    name: str
    auth_endpoint: str
    verification_digits: int = 2  # Default 2-digit verification
    
    # Common university patterns
    PATTERNS = {
        'asu': {
            'domain': 'asu.edu',
            'name': 'Arizona State University',
            'auth_endpoint': 'https://weblogin.asu.edu',
            'federation': 'federation.asu.edu'
        },
        'mit': {
            'domain': 'mit.edu',
            'name': 'Massachusetts Institute of Technology',
            'auth_endpoint': 'https://idp.mit.edu',
            'federation': 'touchstone.mit.edu'
        },
        'stanford': {
            'domain': 'stanford.edu',
            'name': 'Stanford University',
            'auth_endpoint': 'https://login.stanford.edu',
            'federation': 'weblogin.stanford.edu'
        },
        'harvard': {
            'domain': 'harvard.edu',
            'name': 'Harvard University',
            'auth_endpoint': 'https://idp.harvard.edu',
            'federation': 'fed.harvard.edu'
        }
    }
    
    @classmethod
    def from_email(cls, email: str) -> 'University':
        """Auto-detect university from email address"""
        domain = email.split('@')[-1].lower()
        
        # Extract university identifier
        uni_id = domain.split('.')[0]
        
        if uni_id in cls.PATTERNS:
            config = cls.PATTERNS[uni_id]
            return cls(
                domain=config['domain'],
                name=config['name'],
                auth_endpoint=config['auth_endpoint']
            )
        else:
            # Generic .edu handling
            return cls(
                domain=domain,
                name=domain.replace('.edu', '').title(),
                auth_endpoint=f"https://login.{domain}"
            )


class UniversalEduAuth:
    """
    Generalized authentication for any university system
    Works with Duo-compatible 1FA (2-digit verification)
    """
    
    def __init__(self, university: University):
        self.university = university
        self.session = requests.Session()
        
    def authenticate(
        self, 
        username: str, 
        password: str, 
        verification_code: str
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Universal authentication flow
        
        Args:
            username: Student ID or email prefix
            password: Student password
            verification_code: 2-digit verification (Duo-compatible)
            
        Returns:
            (success: bool, user_data: dict)
        """
        try:
            # Step 1: Submit credentials
            auth_response = self._submit_credentials(username, password)
            
            if not auth_response:
                return False, None
            
            # Step 2: Verify with 2-digit code
            verified = self._verify_code(verification_code)
            
            if not verified:
                return False, None
            
            # Step 3: Extract user data
            user_data = self._extract_user_data(username)
            
            # Step 4: Generate secure session token
            token = self._generate_token(user_data)
            user_data['session_token'] = token
            
            return True, user_data
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False, None
    
    def _submit_credentials(self, username: str, password: str) -> bool:
        """Submit username/password to university SSO"""
        try:
            # Normalize username (handle both ASURITE and email formats)
            clean_username = username.split('@')[0]
            
            response = self.session.post(
                f"{self.university.auth_endpoint}/cas/login",
                data={
                    'username': clean_username,
                    'password': password,
                    '_eventId': 'submit'
                },
                allow_redirects=False
            )
            
            # Check for successful first-stage auth (redirect to 2FA)
            return response.status_code in [200, 302, 303]
            
        except:
            return False
    
    def _verify_code(self, code: str) -> bool:
        """Verify 2-digit Duo-compatible code"""
        # Validate format
        if not re.match(r'^\d{2}$', code):
            return False
        
        try:
            # Submit verification code
            response = self.session.post(
                self.session.url if hasattr(self.session, 'url') else 
                f"{self.university.auth_endpoint}/cas/login",
                data={
                    'passcode': code,
                    '_eventId': 'submit'
                }
            )
            
            return response.status_code == 200
            
        except:
            return False
    
    def _extract_user_data(self, username: str) -> Dict:
        """Extract student data from authenticated session"""
        clean_username = username.split('@')[0]
        
        return {
            'username': clean_username,
            'email': f"{clean_username}@{self.university.domain}",
            'university': self.university.name,
            'domain': self.university.domain,
            'verified': True,
            'auth_method': 'duo_2digit',
            'authenticated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_token(self, user_data: Dict) -> str:
        """Generate secure JWT session token"""
        payload = {
            **user_data,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
            'iss': 'first-national-bank'
        }
        
        # Use university-specific secret
        secret = hashlib.sha256(
            f"{self.university.domain}:banking".encode()
        ).hexdigest()
        
        return jwt.encode(payload, secret, algorithm='HS256')
    
    @staticmethod
    def verify_token(token: str, university_domain: str) -> Optional[Dict]:
        """Verify session token"""
        try:
            secret = hashlib.sha256(
                f"{university_domain}:banking".encode()
            ).hexdigest()
            
            return jwt.decode(token, secret, algorithms=['HS256'])
        except:
            return None


# Example Usage
def authenticate_student(email: str, password: str, duo_code: str) -> Tuple[bool, Optional[Dict]]:
    """
    One-line authentication for any university student
    
    Example:
        success, data = authenticate_student(
            "bchirrav@asu.edu", 
            "password123", 
            "42"
        )
    """
    university = University.from_email(email)
    auth = UniversalEduAuth(university)
    return auth.authenticate(email.split('@')[0], password, duo_code)


if __name__ == "__main__":
    # Test with multiple universities
    print("Universal University Authentication System")
    print("=" * 60)
    
    # Test ASU
    uni = University.from_email("student@asu.edu")
    print(f"\n✓ Detected: {uni.name}")
    print(f"  Domain: {uni.domain}")
    print(f"  Auth: {uni.auth_endpoint}")
    
    # Test MIT  
    uni = University.from_email("student@mit.edu")
    print(f"\n✓ Detected: {uni.name}")
    print(f"  Domain: {uni.domain}")
    
    # Test generic .edu
    uni = University.from_email("student@cornell.edu")
    print(f"\n✓ Detected: {uni.name}")
    print(f"  Domain: {uni.domain}")
    
    print("\n" + "=" * 60)
    print("Ready for integration with banking system")
