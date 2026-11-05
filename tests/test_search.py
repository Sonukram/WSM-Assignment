import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ir.engine import SearchEngine
from ir.query_processor import QuerySyntaxError

DOCS = os.path.join(os.path.dirname(__file__), "..", "data", "docs")


class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = SearchEngine(DOCS)

    def names(self, q):
        return [r.name for r in self.e.search(q)]

    def test_case_folding(self):
        self.assertEqual(self.names("QUICK"), ["doc1.txt", "doc4.txt"])

    def test_accent_folding(self):
        self.assertEqual(self.names("cafe"), ["doc3.txt"])

    def test_and_or_not(self):
        self.assertEqual(self.names("quick AND lazy"), ["doc1.txt", "doc4.txt"])
        self.assertEqual(self.names("quick lazy NOT dog"), ["doc4.txt"])
        self.assertEqual(self.names("fox OR index"), ["doc1.txt", "doc2.txt"])
        self.assertEqual(self.names("(fox OR cat) AND lazy"), ["doc1.txt", "doc4.txt"])

    def test_wildcards(self):
        self.assertEqual(self.names("mon*"), ["doc3.txt", "doc4.txt"])
        self.assertEqual(self.names("*key"), ["doc3.txt"])
        self.assertEqual(self.names("m*n*y"), ["doc3.txt"])
        self.assertEqual(self.names("*ndex*"), ["doc2.txt"])

    def test_errors_and_empty(self):
        self.assertEqual(self.names("zzzz"), [])
        with self.assertRaises(QuerySyntaxError):
            self.e.search("(fox")


if __name__ == "__main__":
    unittest.main()
