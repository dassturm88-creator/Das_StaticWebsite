import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello There"          
        actual = extract_title(md)
        self.assertEqual(actual, "Hello There")

    def test_no_header(self):
        md = "just some text\nno title here"
        with self.assertRaises(Exception):
            extract_title(md)

