from unittest import TestCase
from main import blob as tb


class WordListTest(TestCase):

    def test_count(self):
        wl = tb.WordList(['monty', 'python', 'Python', 'Monty'])
        self.assertEqual(wl.count('monty'), None)
        self.assertEqual(wl.count('monty', case_sensitive=True), None)
