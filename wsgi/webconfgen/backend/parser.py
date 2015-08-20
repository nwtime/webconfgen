from .line_parsers import LINE_PARSERS
from .file_parsers import FILE_PARSERS
from .sanity_checkers import SANITY_CHECKERS


class Parser(object):
    def __init__(self, input_file):
        self.input_file = input_file
        object.__init__(self)

    def sanity_check(self):
        for function in SANITY_CHECKERS:
            self.input_file.seek(0)
            if not function(self.input_file):
                return False
        self.input_file.seek(0)
        return True

    def parse(self):
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
