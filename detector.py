"""
Phishing URL Detector (Rule-Based)
Author: Edouardos Stavrakis
Description:
    This script analyzes URLs for common phishing indicators using simple heuristics.
    It outputs a risk score and corresponding risk level based on matched patterns.
"""

import re
import sys
import os
from urllib.parse import urlparse

# ------------------------------
# Detection Heuristics
# ------------------------------

def is_ip_address(domain):
    """Check if domain is an IP address instead of a hostname."""
    return re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain) is not None

def has_many_hyphens(domain):
    """Detect excessive hyphens in domain (used to spoof brands)."""
    return domain.count('-') > 3

def contains_at_symbol(url):
    """Detect '@' symbol which may mislead users."""
    return '@' in url

def contains_suspicious_keywords(url):
    """Check if URL contains common phishing-related keywords."""
    keywords = ['login', 'verify', 'secure', 'account', 'update']
    return [kw for kw in keywords if kw in url.lower()]

def has_suspicious_tld(domain):
    """Flag known suspicious TLDs commonly used in phishing."""
    suspicious_tlds = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top']
    tld = domain.split('.')[-1]
    return tld in suspicious_tlds

def has_encoded_chars(url):
    """Detect URL-encoded characters that may hide intent."""
    return '%' in url

def misleading_subdomain(domain):
    """Detect legit brand names used in subdomains (e.g. paypal.attacker.com)."""
    brands = ['paypal', 'google', 'facebook', 'amazon']
    parts = domain.split('.')
    return any(brand in parts[:-2] for brand in brands)

# ------------------------------
# Core Analysis Logic
# ------------------------------

def analyze_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    result = {
        'uses_ip': is_ip_address(domain),
        'many_hyphens': has_many_hyphens(domain),
        'has_at': contains_at_symbol(url),
        'suspicious_keywords': contains_suspicious_keywords(url),
        'suspicious_tld': has_suspicious_tld(domain),
        'encoded_chars': has_encoded_chars(url),
        'misleading_subdomain': misleading_subdomain(domain)
    }

    return result

# ------------------------------
# Scoring & Output
# ------------------------------

def classify_risk(score):
    if score <= 2:
        return "Low"
    elif score <= 5:
        return "Medium"
    else:
        return "High"

def print_analysis(url, result):
    print(f"\nAnalyzing URL: {url}")
    score = 0

    if result['uses_ip']:
        print("[!] Uses IP address instead of domain.")
        score += 2
    if result['many_hyphens']:
        print("[!] Excessive hyphens in domain.")
        score += 1
    if result['has_at']:
        print("[!] Contains '@' symbol.")
        score += 1
    if result['suspicious_keywords']:
        keywords = ', '.join(result['suspicious_keywords'])
        print(f"[!] Suspicious keywords found: {keywords}")
        score += len(result['suspicious_keywords'])
    if result['suspicious_tld']:
        print("[!] Suspicious top-level domain (TLD).")
        score += 1
    if result['encoded_chars']:
        print("[!] Encoded characters found in URL.")
        score += 1
    if result['misleading_subdomain']:
        print("[!] Brand name found in subdomain (potential spoofing).")
        score += 2

    print(f"Risk Score: {score}/10")
    print(f"Risk Level: {classify_risk(score)}")

# ------------------------------
# Input Handling
# ------------------------------

def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return []
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("http"):
            result = analyze_url(arg)
            print_analysis(arg, result)
        else:
            urls = read_urls_from_file(arg)
            if not urls:
                print("No URLs found in file.")
            for url in urls:
                result = analyze_url(url)
                print_analysis(url, result)
    else:
        print("Usage:")
        print("  python detector.py <url>")
        print("  python detector.py <path-to-url-list.txt>")
        print("\nExamples:")
        print("  python detector.py test_urls.txt")
        print("  python detector.py https://example.com/login")
