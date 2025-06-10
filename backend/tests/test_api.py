import unittest
import json
from api import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_valid_url(self):
        response = self.client.post('/analyze-url',
            data=json.dumps({"url": "http://paypal.login.verify.tk"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("score", data)
        self.assertIn("risk_level", data)
        self.assertEqual(data["risk_level"], "Medium")

    def test_missing_url(self):
        response = self.client.post('/analyze-url',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_invalid_url_format(self):
        response = self.client.post('/analyze-url',
            data=json.dumps({"url": "not-a-url"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("risk_level", response.get_json())

    def test_empty_url(self):
        response = self.client.post('/analyze-url',
            data=json.dumps({"url": ""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_non_http_url(self):
        response = self.client.post('/analyze-url',
            data=json.dumps({"url": "ftp://malicious.example.tk"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("risk_level", response.get_json())
        
    
    def test_generate_email_report(self):
        response = self.client.post('/generate-email-report',
            data=json.dumps({
                "email": "Reset your password here: http://fake-reset.com"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
       
    def test_analyze_email(self):
        payload = {
            "email": "Dear user, We noticed unusual activity in your PayPal account. Please verify your identity immediately by clicking the link: http://paypal.login.verify.tk"
        }
        response = self.client.post(
            "/analyze-email",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("score", data)
        self.assertIn("risk_level", data)
        self.assertIn("indicators", data)
        self.assertEqual(data["risk_level"], "Low")  # Based on basic indicators in example

if __name__ == '__main__':
    unittest.main()