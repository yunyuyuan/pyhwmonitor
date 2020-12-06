from PyQt5 import Qt

btn_list = {
    'cpu': 0xe603,
    'gpu': 0xe604,
    'ram': 0xe605,
    'hdd': 0xe602,
}


class Svg(Qt.QLabel):
    def __init__(self, parent, file, hover=True):
        super().__init__(chr(btn_list[file]), parent)
        self.setProperty('class', 'svg')
        self.setStyleSheet('''
            QLabel{
                font-family: iconfont;
            }
        ''')
        self.hover = hover
