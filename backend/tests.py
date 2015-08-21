"""
Tests for the backend module.
"""

from unittest import TestCase, main

from .file_parsers import FILE_PARSERS
from .line_parsers import LINE_PARSERS
from .sanity_checkers import SANITY_CHECKERS


class SanityCheckTest(TestCase):
    """
        A series of sanity checks
    """
    def test_non_none_parsers(self):
        """
            Tests for non empty parsers.
        """
        self.assertTrue(FILE_PARSERS)
        self.assertTrue(LINE_PARSERS)
        self.assertTrue(SANITY_CHECKERS)


if __name__ == '__main__':
    main()
