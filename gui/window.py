from time import sleep

from PyQt5 import Qt

from components.moveable import Moveable
from components.svg import Svg
from utils.hardware import get_hardware_info, sub_prop
from utils.utils import join_path, screen_size


class Window(Moveable):
    def __init__(self, top):
        super().__init__(flags=Qt.Qt.FramelessWindowHint)
        self.top = top
        self.setup_ui()
        self.setAttribute(Qt.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.Qt.WA_TranslucentBackground)
        layout = Qt.QGridLayout()

        self.frame_background = Qt.QFrame(self)
        self.frame_background.setObjectName('bg')

        self.prop_layout = Qt.QVBoxLayout(self)
        self.prop_elements = []
        self.frame_background.setLayout(self.prop_layout)

        layout.addWidget(self.frame_background)
        self.setLayout(layout)

        self.refresh_thread = Refresh(self)
        self.refresh_thread.start()

        show_pos = self.top.config['pos']
        if len(show_pos) == 0:
            self.show_at_center()
        else:
            self.move(*show_pos)
            self.show()

    def show_at_center(self):
        width, height = screen_size()
        self.move((width - self.width()) // 2, (height - self.height()) // 2)
        self.show()

    def setup_ui(self):
        self.setObjectName("window")
        with open(join_path("static/qss/window.qss"), encoding='utf-8') as fp:
            self.setStyleSheet(fp.read())

    def closeEvent(self, e):
        if self.refresh_thread:
            self.refresh_thread.quit()

    def refresh(self, props_obj):
        # 清除已有的
        while self.prop_layout.count():
            obj = self.prop_layout.itemAt(0).widget()
            if isinstance(obj, Prop):
                obj.setParent(None)
        self.prop_elements = []
        # 新的
        for key in props_obj.keys():
            for item in props_obj[key]:
                element = Prop(self, key, init_value=item['load'], init_info=item, id_=item['id'], keys=sub_prop[key])
                self.prop_elements.append(element)
                self.prop_layout.addWidget(element)
        update_value(self, props_obj)


class Prop(Qt.QFrame):
    def __init__(self, parent, svg, init_value=50, init_info=None, id_='', keys=()):
        super().__init__(parent)
        self.setProperty('class', 'prop')
        self.width_ = 160
        self.height_ = 24
        self.keys = keys
        self.info_rows = []
        self.id_ = id_
        layout = Qt.QHBoxLayout()

        self.svg = Svg(self, svg)

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

        self.info_container = Qt.QFrame(self)
        self.info_container.setProperty('class', 'info-container')
        self.info_layout = Qt.QVBoxLayout()
        for key in self.keys:
            row = Qt.QFrame(self.info_container)
            row.key = key
            row.setProperty('class', 'row')
            row_layout = Qt.QHBoxLayout()

            label_name = Qt.QLabel(key+':', row)
            label_name.setProperty('class', 'name')
            label_name.key = 'name'

            label_value = Qt.QLabel('0', row)
            label_value.setProperty('class', 'value')
            label_value.key = 'value'

            row_layout.addWidget(label_name)
            row_layout.addWidget(label_value)
            row.setLayout(row_layout)
            self.info_layout.addWidget(row)
            self.info_rows.append(row)
        self.info_container.setLayout(self.info_layout)

        layout.setAlignment(Qt.Qt.AlignLeft)
        layout.addWidget(self.svg)
        layout.addWidget(self.value_container)
        layout.addWidget(self.info_container)
        self.setLayout(layout)

        self.update_value(init_value)
        self.update_info(init_info or {})

    def update_value(self, value):
        self.value_crop.setFixedWidth(value*(self.width_-2)/100)

    def update_info(self, info):
        for key in self.keys:
            row = None
            for i in self.info_rows:
                if i.key == key:
                    row = i
            if row:
                for label in row.children():
                    if label.key == 'value':
                        label.setText(str(round(info.get(key, 0), 1)))
                        break


class Refresh(Qt.QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        while True:
            sleep(1)
            props_obj = get_hardware_info(process=True)
            update_value(self.window, props_obj)


def update_value(window_obj, props_obj):
    for key in props_obj.keys():
        for item in props_obj[key]:
            for e in window_obj.prop_elements:
                if e.id_ == item['id']:
                    e.update_value(item['load'])
                    e.update_info(item)
