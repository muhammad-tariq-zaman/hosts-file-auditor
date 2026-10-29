import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import parse_hosts, audit


class TestHostsAuditor(unittest.TestCase):
    def test_parse_skips_comments_and_blanks(self):
        entries = parse_hosts("# comment\n\n127.0.0.1 localhost # trailing\n")
        self.assertEqual(entries, [("127.0.0.1", ["localhost"])])

    def test_invalid_ip_flagged(self):
        self.assertIn("Invalid IP address: 999.1.1.1",
                      audit(parse_hosts("999.1.1.1 badhost\n")))

    def test_duplicate_hostname_different_ip_flagged(self):
        text = "10.0.0.1 web\n10.0.0.2 web\n"
        issues = audit(parse_hosts(text))
        self.assertTrue(any("Duplicate hostname web" in i for i in issues))

    def test_clean_file_has_no_issues(self):
        self.assertEqual(audit(parse_hosts("127.0.0.1 localhost\n::1 localhost\n")), [])


if __name__ == "__main__":
    unittest.main()
