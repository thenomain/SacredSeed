# mygame/commands/tests.py

import unittest
from typeclasses.characters import Character


class TestString(unittest.TestCase):
    """Unittest for strings (just a basic example)."""

    def test_upper(self):
        """Test the upper() str method."""
        self.assertEqual('foo'.upper(), 'FOO')
