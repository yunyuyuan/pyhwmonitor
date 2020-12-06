from PyQt5 import Qt

from components.button import Button
from components.svg import Svg
from utils.utils import join_path


class Setting(Qt.QWidget):
    def __init__(self, top):
        super().__init__()
        self.top = top
        self.setup_ui()

        layout = Qt.QGridLayout()

        prop_layout = Qt.QVBoxLayout()
        # setting
        self.prop_cpu = Prop(self, top, 'cpu', ['温度', '功率'])
        self.prop_gpu = Prop(self, top, 'gpu', ['温度', '功率'])
        prop_layout.addWidget(self.prop_cpu)
        prop_layout.addWidget(self.prop_gpu)

        # button
        button_layout = Qt.QHBoxLayout()
        self.button_about = Button(self, '关于')
        button_layout.addWidget(self.button_about)

        layout.addLayout(prop_layout, 0, 0)
        layout.addLayout(button_layout, 1, 0)
        self.setLayout(layout)
        self.show()

    def closeEvent(self, e):
        self.top.Window.close()

    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setObjectName("setting")
        with open(join_path("static/qss/setting.qss"), encoding='utf-8') as fp:
            self.setStyleSheet(fp.read())


class Prop(Qt.QFrame):
    def __init__(self, parent, top, svg, sub):
        super().__init__(parent)
        self.setProperty("class", "prop")
        self.top = top

        layout = Qt.QGridLayout()

        self.root = Qt.QFrame(self)
        self.root.setProperty('class', "root")
        root_layout = Qt.QVBoxLayout()

        text_label = Qt.QLabel(svg, self.root)
        svg_label = Svg(self.root, svg)

        root_layout.addWidget(text_label)
        root_layout.addWidget(svg_label)
        self.root.setLayout(root_layout)

        layout.addWidget(self.root, 0, 0)
        self.setLayout(layout)
