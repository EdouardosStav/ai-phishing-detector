import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.gpt_summary import generate_gpt_summary

class TestGPTSummary(unittest.TestCase):

    def test_summary_no_api_key(self):
        url = "http://example.com"
        indicators = {"suspicious_keywords": ["login"]}
        risk_level = "medium"
        
        result = generate_gpt_summary(url, indicators, risk_level)
        
        self.assertIn("The URL http://example.com has been assessed", result)
        self.assertIn("suspicious keywords", result)

if __name__ == '__main__':
    unittest.main()