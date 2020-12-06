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
        button_layout.addWidget(self.button_rescan)

        layout.addLayout(self.prop_layout, 0, 0)
        layout.addLayout(button_layout, 1, 0)
        self.setLayout(layout)
        self.show_at_center()

    def show_at_center(self):
        width, height = screen_size()
        self.move((width - self.width()) // 2, (height - self.height()) // 2)
        self.show()

    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setObjectName("setting")
        self.update_qss()

    def update_qss(self):
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
                self.prop_layout.addWidget(Prop(self, self.top, item['name'], key, sub_prop[key], id_=item['id']))
        self.scan_thread = None
        # 通知window
        self.top.Window.refresh(props_obj)


class Prop(Qt.QFrame):
    def __init__(self, parent, top, name, svg, sub, id_):
        super().__init__(parent)
        self.setProperty("class", "prop")
        self.top = top
        self.id_ = id_
        self.set_active()

        layout = Qt.QVBoxLayout()

        self.text_label = Qt.QLabel(name, self)
        self.detail_frame = Qt.QFrame(self)
        self.detail_frame.setProperty('class', 'detail')

        detail_layout = Qt.QHBoxLayout()

        self.svg_label = Svg(self.detail_frame, svg)
        self.svg_label.clicked.connect(self.toggle_prop)
        prop_frame = Qt.QFrame(self.detail_frame)
        prop_frame.setProperty('class', 'sub_props')
        prop_layout = Qt.QHBoxLayout()

        for i in sub:
            sub_p = SubProp(prop_frame, self.top, id_, i)
            prop_layout.addWidget(sub_p)

        prop_frame.setLayout(prop_layout)

        detail_layout.addWidget(self.svg_label)
        detail_layout.addWidget(prop_frame)
        self.detail_frame.setLayout(detail_layout)

        layout.addWidget(self.text_label)
        layout.addWidget(self.detail_frame)
        self.setLayout(layout)

    def set_active(self):
        self.setProperty('active', 't' if self.id_ not in self.top.config['dont_show'] else 'f')

    def toggle_prop(self):
        if self.id_ in self.top.config['dont_show']:
            self.top.config['dont_show'].remove(self.id_)
        else:
            self.top.config['dont_show'].append(self.id_)
        self.top.dump_config()
        self.set_active()
        self.parent().update_qss()
        self.top.Window.refresh()


class SubProp(Qt.QLabel):
    def __init__(self, parent, top, father_id, type_):
        super().__init__(parent)
        self.top = top
        self.setProperty('class', 'sub')
        self.father_id = father_id
        self.type_ = type_
        self.setText(self.top.config['prop_chinese'][type_])
        self.active = not(self.father_id in self.top.config['dont_show_sub'].keys() and \
                      self.type_ in self.top.config['dont_show_sub'][self.father_id])
        self.update_active()

    def update_active(self):
        if self.father_id not in self.top.config['dont_show_sub'].keys():
            self.top.config['dont_show_sub'][self.father_id] = []
        if self.active:
            try:
                self.top.config['dont_show_sub'][self.father_id].remove(self.type_)
            except ValueError:
                pass
        else:
            self.top.config['dont_show_sub'][self.father_id].append(self.type_)
        self.top.dump_config()
        self.setProperty('active', 't' if self.active else 'f')
        self.top.Setting.update_qss()
        for prop in self.top.Window.prop_elements:
            if prop.id_ == self.father_id:
                prop.refresh_info()
                break

    def mousePressEvent(self, e):
        if e.button() == Qt.Qt.LeftButton:
            self.active = not self.active
            self.update_active()
