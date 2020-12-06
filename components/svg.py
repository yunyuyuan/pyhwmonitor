from PyQt5 import Qt

btn_list = {
    'cpu': 0xe3,
    'gpu': 0xe4,
    'ram': 0xe2,
    'hdd': 0xe1,
}


class Svg(Qt.QLabel):
    clicked = Qt.pyqtSignal()

    def __init__(self, parent, file):
        super().__init__(chr(btn_list[file]), parent)
        self.setProperty('class', 'svg')
        self.setStyleSheet('''
            QLabel{
                font-family: iconfont;
            }
        ''')

    def mousePressEvent(self, e):
        if e.button() == Qt.Qt.LeftButton:
            self.clicked.emit()
