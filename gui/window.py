from time import sleep

from PyQt5 import Qt

from components.svg import Svg
from utils.hardware import get_hardware_info
from utils.utils import join_path


class Window(Qt.QWidget):
    def __init__(self, top):
        super().__init__(flags=Qt.Qt.FramelessWindowHint)
        self.top = top
        self.setup_ui()
        self.setAttribute(Qt.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.Qt.WA_TranslucentBackground)
        layout = Qt.QGridLayout()

        self.frame_background = Qt.QFrame(self)
        self.frame_background.setObjectName('bg')

        prop_layout = Qt.QGridLayout(self)
        self.prop_cpu = Prop(self.frame_background, 'cpu')
        self.prop_gpu = Prop(self.frame_background, 'gpu')

        prop_layout.addWidget(self.prop_cpu, 0, 0)
        prop_layout.addWidget(self.prop_gpu, 1, 0)
        self.frame_background.setLayout(prop_layout)

        layout.addWidget(self.frame_background)
        self.setLayout(layout)
        self.show()

        self.refresh_thread = Refresh(self)
        self.refresh_thread.start()

    def setup_ui(self):
        self.setObjectName("window")
        with open(join_path("static/qss/window.qss"), encoding='utf-8') as fp:
            self.setStyleSheet(fp.read())

    def closeEvent(self, e):
        if self.refresh_thread:
            self.refresh_thread.quit()


class Prop(Qt.QFrame):
    def __init__(self, parent, svg):
        super().__init__(parent)
        self.setProperty('class', 'prop')
        self.value = 0
        self.width_ = 160
        self.height_ = 24
        self.info = {}
        layout = Qt.QGridLayout()

        self.svg = Svg(self, svg, False)

        self.value_container = Qt.QFrame(self)
        self.value_container.setProperty('class', 'value-container')
        value_layout = Qt.QVBoxLayout()

        self.value_crop = Qt.QLabel(self.value_container)
        self.value_crop.setProperty('class', 'crop')
        self.value_crop.setFixedHeight(self.height_-2)

        self.value_content = Qt.QLabel(self.value_crop)
        self.value_content.setProperty('class', 'content')
        self.value_content.move(0, 0)
        self.value_content.setFixedSize(self.width_, self.height_-2)

        value_layout.addWidget(self.value_crop)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(0)
        self.value_container.setLayout(value_layout)
        self.value_container.setFixedSize(self.width_, self.height_)

        layout.addWidget(self.svg, 0, 0)
        layout.addWidget(self.value_container, 0, 1)
        self.setLayout(layout)

        self.update_value(50)

    def update_value(self, value):
        self.value = value
        self.value_crop.setFixedWidth(self.value*(self.width_-2)/100)

    def update_info(self, info):
        self.info = info


class Refresh(Qt.QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        while True:
            sleep(1)
            lis = get_hardware_info()
            for i in lis:
                if i['type'] == 'cpu':
                    for j in i['data']:
                        if j['name'] == 'CPU Total' and j['type'] == 'Load':
                            self.window.prop_cpu.update_value(j['value'])
                            break

                    else:
                        break
                elif i['type-idx'] == 4:
                    for j in i['data']:
                        if j['name'] == 'GPU Core' and j['type'] == 'Load':
                            self.window.prop_gpu.update_value(j['value'])
                            break

                    else:
                        break
