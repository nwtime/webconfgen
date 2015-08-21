"""
Functions for file parser are defined here.

File parsers are very powerful and allow entire files to
be dramatically changed.

As such, the edits are to be kept minimal.

The returned output is passed through each of the parsers

The FILE_PARSERS are to be registered as
    {
        function,
        function,
    }

TODO: Implement version based parsing.
"""


import datetime


def add_parse_date(output):
    """
        Adds the parsing date on the top of
        the file as a comment.
    """
    return "# " + str(datetime.datetime.now()) + "\n" + output

FILE_PARSERS = [
    add_parse_date,
]
