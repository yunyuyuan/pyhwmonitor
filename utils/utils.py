from os import getcwd
from os.path import join
from PyQt5 import Qt


def join_path(s):
    return join(getcwd(), s)


def screen_size():
    desktop = Qt.QApplication.desktop().screen()
    return desktop.width(), desktop.height()
