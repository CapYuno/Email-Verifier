import re
import socket
import dns.resolver
import requests

class EmailVerifier:
    """
    A class to verify email addresses using multiple validation methods
    without actually sending emails.
    """
    
    def __init__(self):
        # Common disposable email domains
        self.disposable_domains_url = "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/domains.json"
        self.disposable_domains = self._load_disposable_domains()
    
    def _load_disposable_domains(self):
        """Load list of disposable email domains from GitHub repository"""
        try:
            response = requests.get(self.disposable_domains_url)
            if response.status_code == 200:
                return set(response.json())
            return set()
        except Exception:
            # If unable to fetch, return an empty set
            return set()
    
    def verify_syntax(self, email):
        """
        Verify if the email has valid syntax according to RFC 5322
        
        Args:
            email (str): Email address to verify
            
        Returns:
            bool: True if syntax is valid, False otherwise
        """
        # Regular expression for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def verify_domain(self, email):
        """
        Verify if the domain in the email exists
        
        Args:
            email (str): Email address to verify
            
        Returns:
            bool: True if domain exists, False otherwise
        """
        try:
            domain = email.split('@')[1]
            socket.gethostbyname(domain)
            return True
        except (IndexError, socket.gaierror):
            return False
    
    def verify_mx_record(self, email):
        """
        Verify if the domain has MX records (mail exchange servers)
        
        Args:
            email (str): Email address to verify
            
        Returns:
            bool: True if MX records exist, False otherwise
        """
        try:
            domain = email.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except (IndexError, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            return False
    
    def is_disposable(self, email):
        """
        Check if the email uses a disposable domain
        
        Args:
            email (str): Email address to check
            
        Returns:
            bool: True if the email uses a disposable domain, False otherwise
        """
        try:
            domain = email.split('@')[1]
            return domain in self.disposable_domains
        except IndexError:
            return False
    
    def verify_email(self, email):
        """
        Perform all verification checks on an email
        
        Args:
            email (str): Email address to verify
            
        Returns:
            dict: Results of all verification checks
        """
        results = {
            "email": email,
            "is_valid_syntax": False,
            "domain_exists": False,
            "has_mx_record": False,
            "is_disposable": False,
            "overall_score": 0,  # 0-100 score
            "is_likely_valid": False
        }
        
        # Check syntax first
        results["is_valid_syntax"] = self.verify_syntax(email)
        if not results["is_valid_syntax"]:
            return results
        
        # Check domain
        results["domain_exists"] = self.verify_domain(email)
        
        # Check MX records
        results["has_mx_record"] = self.verify_mx_record(email)
        
        # Check if disposable
        results["is_disposable"] = self.is_disposable(email)
        
        # Calculate overall score
        score = 0
        if results["is_valid_syntax"]:
            score += 25
        if results["domain_exists"]:
            score += 25
        if results["has_mx_record"]:
            score += 25
        if not results["is_disposable"]:
            score += 25
            
        results["overall_score"] = score
        results["is_likely_valid"] = score >= 75
        
        return results