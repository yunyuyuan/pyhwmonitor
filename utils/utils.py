from os import getcwd
from os.path import join


def join_path(s):
    return join(getcwd(), s)
