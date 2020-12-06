from PyQt5 import Qt

from components.button import Button
from components.svg import Svg
from utils.hardware import get_hardware_info, ReScan, sub_prop
from utils.utils import join_path, screen_size


class Setting(Qt.QWidget):
    def __init__(self, top):
        super().__init__()
        self.top = top
        self.setup_ui()
        self.scan_thread = None

        layout = Qt.QGridLayout()

        self.prop_layout = Qt.QVBoxLayout()
        # props
        self.scan()

        # button
        button_layout = Qt.QHBoxLayout()
        self.button_rescan = Button(self, '刷新', lambda e: self.scan())
        self.button_about = Button(self, '关于')
        button_layout.addWidget(self.button_rescan)
        button_layout.addWidget(self.button_about)

        layout.addLayout(self.prop_layout, 0, 0)
        layout.addLayout(button_layout, 1, 0)
        self.setLayout(layout)
        self.show_at_center()

    def show_at_center(self):
        width, height = screen_size()
        self.move((width-self.width())//2, (height-self.height())//2)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setObjectName("setting")
        with open(join_path("static/qss/setting.qss"), encoding='utf-8') as fp:
            self.setStyleSheet(fp.read())

    def closeEvent(self, e):
        self.top.Window.close()

    def scan(self):
        if self.scan_thread:
            return
        self.scan_thread = ReScan(self)
        # 删除旧元素
        while self.prop_layout.count():
            obj = self.prop_layout.itemAt(0).widget()
            if isinstance(obj, Prop):
                obj.setParent(None)
        self.scan_thread.start()
        self.scan_thread.finished.connect(self.refresh)

    def refresh(self):
        props_obj = get_hardware_info(process=True)
        for key in props_obj.keys():
            for item in props_obj[key]:
                self.prop_layout.addWidget(Prop(self, self.top, item['name'], key, sub_prop[key]))
        self.scan_thread = None
        # 通知window
        self.top.Window.refresh(props_obj)


class Prop(Qt.QFrame):
    def __init__(self, parent, top, name, svg, sub):
        super().__init__(parent)
        self.setProperty("class", "prop")
        self.top = top

        layout = Qt.QGridLayout()

        self.root = Qt.QFrame(self)
        self.root.setProperty('class', "root")
        root_layout = Qt.QVBoxLayout()

        text_label = Qt.QLabel(name, self.root)
        svg_label = Svg(self.root, svg)

        root_layout.addWidget(text_label)
        root_layout.addWidget(svg_label)
        self.root.setLayout(root_layout)

        layout.addWidget(self.root, 0, 0)
        self.setLayout(layout)
