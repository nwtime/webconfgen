from .line_parsers import LINE_PARSERS


class Parser(object):
    def __init__(self, input_file):
        self.input_file = input_file
        object.__init__(self)

    def sanity_check(self):
        pass

    def parse(self):
        self.sanity_check()
        output_list = []
        for line in self.input_file:
            for compiled_pattern, function in LINE_PARSERS.iteritems():
                if compiled_pattern.match(line):
                    line = function(line)
            output_list.append(line)

        return "".join(output_list)
