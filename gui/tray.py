from PyQt5 import Qt


class Tray(Qt.QSystemTrayIcon):
    def __init__(self, top):
        super().__init__()
        self.top = top

