"""
Autonomous CVE Monitoring and Security Bolstering System
- Daily CVE scanning from NVD, Grafana, GitHub Security Advisories
- Automatic security patch application
- Grafana security release integration
- Continuous security posture improvement
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import subprocess
import re
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class CVE:
    """CVE vulnerability data"""
    cve_id: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    cvss_score: float
    published_date: str
    affected_packages: List[str]
    fixed_version: Optional[str]
    source: str  # NVD, Grafana, GitHub, etc.
    patch_available: bool = False
    auto_patchable: bool = False
    
    def __hash__(self):
        return hash(self.cve_id)


class CVEMonitor:
    """Autonomous CVE monitoring system"""
    
    # Data sources
    NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    GRAFANA_SECURITY = "https://grafana.com/api/security/advisories"
    GITHUB_ADVISORIES = "https://api.github.com/advisories"
    
    def __init__(self, app_dependencies: List[str]):
        """
        Initialize CVE monitor
        
        Args:
            app_dependencies: List of packages (e.g., ['flask==3.0.3', 'sqlalchemy==2.0.30'])
        """
        self.dependencies = self._parse_dependencies(app_dependencies)
        self.cve_database = set()
        self.last_scan = None
        
    def _parse_dependencies(self, deps: List[str]) -> Dict[str, str]:
        """Parse dependency list into package:version dict"""
        parsed = {}
        for dep in deps:
            match = re.match(r'([a-zA-Z0-9\-_]+)[=<>]+(.+)', dep)
            if match:
                package, version = match.groups()
                parsed[package.lower()] = version
        return parsed
    
    async def scan_daily(self) -> List[CVE]:
        """
        Daily autonomous CVE scan
        Runs automatically, returns new vulnerabilities
        """
        print(f"\n{'='*60}")
        print(f"CVE Daily Scan - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        new_cves = []
        
        # Scan all sources
        new_cves.extend(await self._scan_nvd())
        new_cves.extend(await self._scan_grafana())
        new_cves.extend(await self._scan_github())
        new_cves.extend(await self._scan_python_safety())
        
        # Deduplicate
        unique_cves = {cve.cve_id: cve for cve in new_cves}
        new_cves = list(unique_cves.values())
        
        # Filter for our dependencies
        relevant_cves = self._filter_relevant(new_cves)
        
        # Update database
        self.cve_database.update(relevant_cves)
        self.last_scan = datetime.now()
        
        # Log results
        print(f"Total CVEs found: {len(new_cves)}")
        print(f"Relevant to our app: {len(relevant_cves)}")
        print(f"Critical: {sum(1 for c in relevant_cves if c.severity == 'CRITICAL')}")
        print(f"High: {sum(1 for c in relevant_cves if c.severity == 'HIGH')}")
        
        return list(relevant_cves)
    
    async def _scan_nvd(self) -> List[CVE]:
        """Scan NVD database for recent CVEs"""
        try:
            # Get CVEs from last 24 hours
            now = datetime.now()
            yesterday = now - timedelta(days=1)
            
            params = {
                'pubStartDate': yesterday.strftime('%Y-%m-%dT%H:%M:%S.000'),
                'pubEndDate': now.strftime('%Y-%m-%dT%H:%M:%S.000')
            }
            
            response = requests.get(self.NVD_API, params=params, timeout=30)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            cves = []
            
            for item in data.get('vulnerabilities', []):
                cve_data = item.get('cve', {})
                
                # Extract CVSS score
                metrics = cve_data.get('metrics', {})
                cvss_data = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
                cvss_score = cvss_data.get('baseScore', 0.0)
                
                # Map score to severity
                if cvss_score >= 9.0:
                    severity = 'CRITICAL'
                elif cvss_score >= 7.0:
                    severity = 'HIGH'
                elif cvss_score >= 4.0:
                    severity = 'MEDIUM'
                else:
                    severity = 'LOW'
                
                # Extract description
                descriptions = cve_data.get('descriptions', [])
                description = descriptions[0].get('value', '') if descriptions else ''
                
                cve = CVE(
                    cve_id=cve_data.get('id', ''),
                    description=description[:500],
                    severity=severity,
                    cvss_score=cvss_score,
                    published_date=cve_data.get('published', ''),
                    affected_packages=self._extract_packages(description),
                    fixed_version=None,
                    source='NVD'
                )
                cves.append(cve)
            
            return cves
            
        except Exception as e:
            print(f"NVD scan error: {e}")
            return []
    
    async def _scan_grafana(self) -> List[CVE]:
        """Scan Grafana security advisories"""
        try:
            response = requests.get(self.GRAFANA_SECURITY, timeout=30)
            
            if response.status_code != 200:
                return []
            
            advisories = response.json()
            cves = []
            
            for advisory in advisories:
                # Check if published in last 24 hours
                pub_date = datetime.fromisoformat(advisory.get('published', '').replace('Z', '+00:00'))
                if (datetime.now() - pub_date.replace(tzinfo=None)).days > 1:
                    continue
                
                cve = CVE(
                    cve_id=advisory.get('cve_id', f"GRAFANA-{advisory.get('id')}"),
                    description=advisory.get('summary', ''),
                    severity=advisory.get('severity', 'MEDIUM').upper(),
                    cvss_score=advisory.get('cvss_score', 0.0),
                    published_date=advisory.get('published', ''),
                    affected_packages=['grafana'],
                    fixed_version=advisory.get('fixed_version'),
                    source='Grafana',
                    patch_available=bool(advisory.get('fixed_version'))
                )
                cves.append(cve)
            
            return cves
            
        except Exception as e:
            print(f"Grafana scan error: {e}")
            return []
    
    async def _scan_github(self) -> List[CVE]:
        """Scan GitHub Security Advisories"""
        try:
            headers = {'Accept': 'application/vnd.github+json'}
            response = requests.get(self.GITHUB_ADVISORIES, headers=headers, timeout=30)
            
            if response.status_code != 200:
                return []
            
            advisories = response.json()
            cves = []
            
            for advisory in advisories[:50]:  # Limit to recent 50
                # Check if recent
                pub_date = datetime.fromisoformat(advisory.get('published_at', '').replace('Z', '+00:00'))
                if (datetime.now() - pub_date.replace(tzinfo=None)).days > 1:
                    continue
                
                cve = CVE(
                    cve_id=advisory.get('cve_id') or advisory.get('ghsa_id', ''),
                    description=advisory.get('summary', ''),
                    severity=advisory.get('severity', 'MEDIUM').upper(),
                    cvss_score=advisory.get('cvss', {}).get('score', 0.0),
                    published_date=advisory.get('published_at', ''),
                    affected_packages=[advisory.get('package', {}).get('name', '')],
                    fixed_version=None,
                    source='GitHub'
                )
                cves.append(cve)
            
            return cves
            
        except Exception as e:
            print(f"GitHub scan error: {e}")
            return []
    
    async def _scan_python_safety(self) -> List[CVE]:
        """Scan Python Safety DB for dependency vulnerabilities"""
        try:
            # Use safety check command
            result = subprocess.run(
                ['safety', 'check', '--json', '--key', 'free'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0 and not result.stdout:
                return []
            
            data = json.loads(result.stdout)
            cves = []
            
            for vuln in data:
                cve = CVE(
                    cve_id=vuln.get('cve', f"SAFETY-{vuln.get('id')}"),
                    description=vuln.get('advisory', ''),
                    severity='HIGH',  # Safety DB doesn't provide severity
                    cvss_score=7.0,
                    published_date=datetime.now().isoformat(),
                    affected_packages=[vuln.get('package', '')],
                    fixed_version=vuln.get('fixed_version'),
                    source='Safety DB',
                    patch_available=True,
                    auto_patchable=True
                )
                cves.append(cve)
            
            return cves
            
        except:
            return []
    
    def _extract_packages(self, text: str) -> List[str]:
        """Extract package names from CVE description"""
        # Common Python packages
        packages = []
        for pkg in self.dependencies.keys():
            if pkg.lower() in text.lower():
                packages.append(pkg)
        return packages
    
    def _filter_relevant(self, cves: List[CVE]) -> List[CVE]:
        """Filter CVEs relevant to our dependencies"""
        relevant = []
        for cve in cves:
            for package in cve.affected_packages:
                if package.lower() in self.dependencies:
                    relevant.append(cve)
                    break
        return relevant


class AutoPatcher:
    """Autonomous security patch application"""
    
    def __init__(self, monitor: CVEMonitor):
        self.monitor = monitor
        self.applied_patches = []
        
    async def auto_patch(self, cves: List[CVE]) -> Dict:
        """
        Automatically apply security patches
        
        Returns:
            Dict with patch results
        """
        print(f"\n{'='*60}")
        print("Auto-Patching System")
        print(f"{'='*60}\n")
        
        results = {
            'attempted': 0,
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        # Sort by severity
        cves_sorted = sorted(cves, key=lambda x: (
            {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}.get(x.severity, 0)
        ), reverse=True)
        
        for cve in cves_sorted:
            if not cve.auto_patchable:
                continue
            
            results['attempted'] += 1
            
            # Attempt patch
            success = await self._apply_patch(cve)
            
            if success:
                results['successful'] += 1
                self.applied_patches.append(cve)
                print(f"✓ Patched: {cve.cve_id} ({cve.affected_packages[0]})")
            else:
                results['failed'] += 1
                print(f"✗ Failed: {cve.cve_id}")
            
            results['details'].append({
                'cve_id': cve.cve_id,
                'package': cve.affected_packages[0] if cve.affected_packages else 'unknown',
                'success': success
            })
        
        print(f"\nPatch Summary:")
        print(f"  Attempted: {results['attempted']}")
        print(f"  Successful: {results['successful']}")
        print(f"  Failed: {results['failed']}")
        
        return results
    
    async def _apply_patch(self, cve: CVE) -> bool:
        """Apply individual security patch"""
        try:
            if not cve.affected_packages or not cve.fixed_version:
                return False
            
            package = cve.affected_packages[0]
            version = cve.fixed_version
            
            # Update package
            result = subprocess.run(
                ['pip', 'install', '--upgrade', f'{package}=={version}'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return result.returncode == 0
            
        except:
            return False


# Integration with Banking App
async def run_daily_security_scan(app_dependencies: List[str]):
    """
    Main entry point for daily security scanning
    Run this as a cron job or scheduled task
    """
    # Initialize monitor
    monitor = CVEMonitor(app_dependencies)
    
    # Scan for CVEs
    new_cves = await monitor.scan_daily()
    
    # Auto-patch critical/high severity
    patcher = AutoPatcher(monitor)
    critical_high = [c for c in new_cves if c.severity in ['CRITICAL', 'HIGH']]
    
    if critical_high:
        patch_results = await patcher.auto_patch(critical_high)
        
        # Log to file
        with open('security_scan_results.json', 'w') as f:
            json.dump({
                'scan_date': datetime.now().isoformat(),
                'cves_found': len(new_cves),
                'critical_high': len(critical_high),
                'patches_applied': patch_results['successful'],
                'details': [asdict(cve) for cve in new_cves]
            }, f, indent=2)
    
    return new_cves, patch_results if critical_high else None


if __name__ == "__main__":
    import asyncio
    
    # Example: Banking app dependencies
    dependencies = [
        'Flask==3.0.3',
        'SQLAlchemy==2.0.30',
        'argon2-cffi==23.1.0',
        'PyJWT==2.8.0',
        'cryptography==42.0.7',
        'redis==5.0.4',
        'psycopg2-binary==2.9.9'
    ]
    
    # Run daily scan
    asyncio.run(run_daily_security_scan(dependencies))
