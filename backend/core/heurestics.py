import re
from urllib.parse import urlparse

def is_ip_address(domain):
    return re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain) is not None

def has_many_hyphens(domain):
    return domain.count('-') > 3

def contains_at_symbol(url):
    return '@' in url

def contains_suspicious_keywords(url):
    keywords = ['login', 'verify', 'secure', 'account', 'update']
    return [kw for kw in keywords if kw in url.lower()]

def has_suspicious_tld(domain):
    suspicious_tlds = ['tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top']
    return domain.split('.')[-1] in suspicious_tlds

def has_encoded_chars(url):
    return '%' in url

def misleading_subdomain(domain):
    brands = ['paypal', 'google', 'facebook', 'amazon']
    parts = domain.split('.')
    return any(brand in parts[:-2] for brand in brands)

def analyze_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    return {
        'uses_ip': is_ip_address(domain),
        'many_hyphens': has_many_hyphens(domain),
        'has_at': contains_at_symbol(url),
        'suspicious_keywords': contains_suspicious_keywords(url),
        'suspicious_tld': has_suspicious_tld(domain),
        'encoded_chars': has_encoded_chars(url),
        'misleading_subdomain': misleading_subdomain(domain)
    }

def calculate_score(result):
    score = 0
    if result['uses_ip']: score += 2
    if result['many_hyphens']: score += 1
    if result['has_at']: score += 1
    if result['suspicious_keywords']: score += len(result['suspicious_keywords'])
    if result['suspicious_tld']: score += 1
    if result['encoded_chars']: score += 1
    if result['misleading_subdomain']: score += 2
    return score

def classify_risk(score):
    if score <= 2: return "Low"
    elif score <= 5: return "Medium"
    else: return "High"