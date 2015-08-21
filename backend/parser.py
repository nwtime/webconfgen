"""
Implements a Parser for the calling of LINE_PARSERS, FILE_PARSERS and SANITY_CHECKERS functions.

TODO: Add version based parsing.
"""


from .file_parsers import FILE_PARSERS
from .line_parsers import LINE_PARSERS
from .sanity_checkers import SANITY_CHECKERS


class Parser(object):
    """
        A parser class which takes the input_file as the input and parses it
        in accordence with the LINE_PARSERS and FILE_PARSERS.
    """
    def __init__(self, input_file):
        """
        TODO: Add version based parsing.
        """
        self.input_file = input_file
        object.__init__(self)

    def sanity_check(self):
        """
            Performs a sanity check on the file.
        """
        for function in SANITY_CHECKERS:
            self.input_file.seek(0)
            if not function(self.input_file):
                return False
        self.input_file.seek(0)
        return True

    def parse(self):
        """
            Parses based on the input, and returns
            a string output.
        """
        if not self.sanity_check():
            return "File is Insane!"

        output_list = []
        for line in self.input_file:
            for compiled_pattern, function in LINE_PARSERS.iteritems():
                if compiled_pattern.match(line):
                    line = function(line)
            output_list.append(line)
        output = "".join(output_list)

        for function in FILE_PARSERS:
            output = function(output)

        return output
