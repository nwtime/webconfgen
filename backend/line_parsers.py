"""
Functions for per line parser are defined here.

The pre-compiled rejex ensures that only strings which
are suitable for parsing are used.

The LINE_PARSERS are to be registered as
    {
        compiled_regex: function,
        compiled_regex: function,
    }
"""


import re


def replace_snippet_3(line):
    """
        A dummy parser which returns a line + 'Parsed'
        when the 'Snippet 3' regex is matched.
    """
    return line + " Parsed"

LINE_PARSERS = {
    re.compile('Snippet 3'): replace_snippet_3,
}
