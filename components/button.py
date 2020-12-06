from PyQt5 import Qt


class Button(Qt.QPushButton):
    def __init__(self, parent, text, cb=lambda event: 0):
        super().__init__(parent, text=text)
        self.cb = cb
        self.clicked.connect(self.onclick)

    def onclick(self, e):
        self.cb(e)
