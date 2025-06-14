import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.pdf_generator import generate_email_pdf_report, generate_pdf_report

class TestPDFGenerator(unittest.TestCase):

    def test_generate_pdf(self):
        path = "test_report.pdf"
        indicators = {
            "suspicious_keywords": ["login"],
            "suspicious_tld": True,
            "misleading_subdomain": False
        }
        report_path = generate_pdf_report(
            url="http://example.com",
            indicators=indicators,
            score=3,
            risk_level="Medium",
            gpt_summary="This is a test summary.",
            output_path=path
        )
        self.assertTrue(os.path.exists(report_path))
        os.remove(report_path)
        
class TestEmailPDFGenerator(unittest.TestCase):

    def test_generate_email_pdf(self):
        indicators = {
            "suspicious_phrases": ["verify your account"],
            "contains_link": True,
            "has_encoded_chars": False
        }

        output = "test_email_report.pdf"
        path = generate_email_pdf_report(
            "Your account is suspended. Visit http://link.com",
            indicators,
            4,
            "Medium",
            "Test AI explanation.",
            output_path=output
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)

if __name__ == '__main__':
    unittest.main()