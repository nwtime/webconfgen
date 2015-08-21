"""
Sanity Checks Module

Functions for sanity checking are to be listed here.
The functions registered with the SANITY_CHECKERS list
are executed as sanity checks for the parsing of a file.

TODO: Add support for version based filtering.
"""


from binaryornot.helpers import is_binary_string


def insane_should_not_be_substring(input_file):
    """
        A dummy parsing where any file having substring 'insane'
        is declared to be insane file.
    """
    if 'insane' in input_file.read():
        return False
    return True


def is_binary_wrapper(input_file):
    """
        Uses the binaryornot package to check if the uploaded file
        is binary or not.

        Declares a file to be insane if it is detected to be binary.
    """
    chunk = input_file.read(1024)
    return not is_binary_string(chunk)

SANITY_CHECKERS = [
    insane_should_not_be_substring,
    is_binary_wrapper,
]
