from PyQt5 import Qt


class Moveable(Qt.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_start = []
        self.move_start = []
        self.moving = False

    def mousePressEvent(self, e):
        self.moving = True
        self.pos_start = self.pos()
        self.move_start = e.globalPos()

    def mouseReleaseEvent(self, e):
        self.moving = False
        self.move_end()

    def mouseMoveEvent(self, e):
        if self.moving:
            pos_now = e.globalPos()
            delta = (pos_now.x()-self.move_start.x(), pos_now.y()-self.move_start.y())
            target_pos = (self.pos_start.x()+delta[0], self.pos_start.y()+delta[1])
            self.move(*target_pos)

    def move_end(self):
        pass
