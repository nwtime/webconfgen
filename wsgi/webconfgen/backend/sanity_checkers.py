from binaryornot.helpers import is_binary_string


def insane_should_not_be_substring(input_file):
    if 'insane' in input_file.read():
        return False
    return True


def is_binary_wrapper(input_file):
    chunk = input_file.read(1024)
    print chunk
    return not is_binary_string(chunk)

SANITY_CHECKERS = [
    insane_should_not_be_substring,
    is_binary_wrapper,
]
