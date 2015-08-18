import re


def replace_snippet_3(line):
    return line + " Parsed"

LINE_PARSERS = {
    re.compile('Snippet 3'): replace_snippet_3,
}
