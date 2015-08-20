import datetime


def add_parse_date(output):
    return "# " + str(datetime.datetime.now()) + "\n" + output

FILE_PARSERS = [
    add_parse_date,
]
