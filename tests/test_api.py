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

if __name__ == '__main__':
    unittest.main()
