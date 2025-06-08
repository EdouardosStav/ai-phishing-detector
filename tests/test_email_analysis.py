import unittest
from core.email_analysis import analyze_email_text, calculate_email_score

class TestEmailAnalysis(unittest.TestCase):

    def test_suspicious_email_with_link(self):
        text = "Please verify your account here: http://fake-link.com"
        result = analyze_email_text(text)
        self.assertIn("verify your account", result['suspicious_phrases'])
        self.assertTrue(result['contains_link'])
        self.assertFalse(result['has_encoded_chars'])

    def test_encoded_characters(self):
        text = "Reset password: https://secure.com/%2Flogin"
        result = analyze_email_text(text)
        self.assertTrue(result['has_encoded_chars'])
        self.assertTrue(result['contains_link'])

    def test_clean_email(self):
        text = "Welcome to our newsletter."
        result = analyze_email_text(text)
        self.assertFalse(result['suspicious_phrases'])
        self.assertFalse(result['contains_link'])
        self.assertFalse(result['has_encoded_chars'])
        
class TestEmailScore(unittest.TestCase):

    def test_all_indicators(self):
        indicators = {
            "suspicious_phrases": ["verify your account", "click the link"],
            "contains_link": True,
            "has_encoded_chars": True
        }
        score = calculate_email_score(indicators)
        self.assertEqual(score, 6)  # 2 phrases + 2 (link) + 2 (obfuscation)

    def test_empty_indicators(self):
        indicators = {
            "suspicious_phrases": [],
            "contains_link": False,
            "has_encoded_chars": False
        }
        score = calculate_email_score(indicators)
        self.assertEqual(score, 0)

if __name__ == '__main__':
    unittest.main()