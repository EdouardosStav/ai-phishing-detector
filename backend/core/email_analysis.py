def analyze_email_text(text):
    indicators = {
        'suspicious_phrases': [],
        'contains_link': False,
        'has_encoded_chars': False
    }
    suspicious_keywords = ["verify your account", "login here", "click the link", "password reset", "urgent"]

    for phrase in suspicious_keywords:
        if phrase in text.lower():
            indicators['suspicious_phrases'].append(phrase)

    if "http://" in text or "https://" in text:
        indicators['contains_link'] = True

    if "%2F" in text or "%3A" in text:
        indicators['has_encoded_chars'] = True

    return indicators

def calculate_email_score(indicators):
    score = 0
    if indicators.get("suspicious_phrases"):
        score += len(indicators["suspicious_phrases"])
    if indicators.get("contains_link"):
        score += 2
    if indicators.get("has_encoded_chars"):
        score += 2
    return min(score, 10)