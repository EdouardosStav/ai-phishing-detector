import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.heurestics import (
    is_ip_address,
    has_many_hyphens,
    contains_at_symbol,
    contains_suspicious_keywords,
    has_suspicious_tld,
    has_encoded_chars,
    misleading_subdomain
)

class TestHeuristics(unittest.TestCase):
    def test_is_ip_address(self):
        self.assertTrue(is_ip_address("192.168.0.1"))
        self.assertFalse(is_ip_address("example.com"))

    def test_has_many_hyphens(self):
        self.assertTrue(has_many_hyphens("this-is-a-bad-domain.com"))
        self.assertFalse(has_many_hyphens("normaldomain.com"))

    def test_contains_at_symbol(self):
        self.assertTrue(contains_at_symbol("http://example.com@evil.com"))
        self.assertFalse(contains_at_symbol("https://example.com"))

    def test_contains_suspicious_keywords(self):
        self.assertIn("login", contains_suspicious_keywords("https://secure-login.com"))
        self.assertEqual(contains_suspicious_keywords("https://safe.com"), [])

    def test_has_suspicious_tld(self):
        self.assertTrue(has_suspicious_tld("example.tk"))
        self.assertFalse(has_suspicious_tld("example.com"))

    def test_has_encoded_chars(self):
        self.assertTrue(has_encoded_chars("http://site.com/%2Flogin"))
        self.assertFalse(has_encoded_chars("http://site.com/login"))

    def test_misleading_subdomain(self):
        self.assertTrue(misleading_subdomain("paypal.attacker.com"))
        self.assertFalse(misleading_subdomain("secure.paypal.com"))

if __name__ == '__main__':
    unittest.main()
