from PyQt5 import Qt
from json import load, dump

from gui.setting import Setting
from gui.tray import Tray
from gui.window import Window

from utils.utils import join_path


class App:
    def __init__(self):
        self.config_path = join_path('utils/config.json')
        font_id = Qt.QFontDatabase.addApplicationFont(join_path("static/iconfont.ttf"))
        self.ico_font = Qt.QFont(Qt.QFontDatabase.applicationFontFamilies(font_id)[0], 30)
        self.config = {}
        self.load_config()
        self.Setting = Setting(self)
        self.Window = Window(self)
        self.Tray = Tray(self)

        if self.config['show_setting_window']:
            self.Setting.show()
            self.config['show_setting_window'] = False
            self.dump_config()

    def load_config(self):
        with open(self.config_path, encoding='utf-8') as fp:
            self.config = load(fp)

    def dump_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as fp:
            dump(self.config, fp, indent=4)


if __name__ == '__main__':
    from sys import argv
    a = Qt.QApplication(argv)
    app = App()
    a.exec_()
