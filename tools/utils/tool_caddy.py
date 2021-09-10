import json
import os

from PySide2.QtWidgets import QComboBox, QLabel, QWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QSettings
from tools.ui.ad_widgets import MayaWidget, VBoxLayout, Widget
from tools.ui import dockable_widget
from functools import partial


class ToolCaddy(MayaWidget):
    TITLE = 'Tool Caddy'
    JSON_PATH = os.path.join(os.path.dirname(__file__), 'tool_caddy.json')
    all = 'All'

    def __init__(self):
        super(ToolCaddy, self).__init__(self.TITLE)
        with open(self.JSON_PATH) as f:
            self.tool_data = json.load(f)
        self.settings = QSettings('robosoft', 'tool_caddy')
        self.filter = self.settings.value('filter', self.all)
        self.combo_box = QComboBox()
        self.button_widget = Widget()
        self.script_widget = Widget()
        self.status_bar = QLabel('Ready')
        self.add_widget(self.combo_box)
        self.add_widget(self.script_widget)
        self.add_widget(self.status_bar)
        self.init_combo_box()
        self.refresh_buttons()
        self.setMinimumWidth(320)

    def init_combo_box(self):
        self.combo_box.clear()
        tool_keys = list(self.tool_data.keys())
        tool_keys.sort(key=lambda x: x.lower())
        self.combo_box.addItems([self.all] + tool_keys)
        self.combo_box.setCurrentText(self.filter)
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)

    def combo_box_changed(self):
        self.filter = self.combo_box.currentText()
        self.status_bar.setText(f"Filter changed to {self.filter}")
        self.settings.setValue('filter', self.filter)
        self.refresh_buttons()

    def refresh_buttons(self):
        self.script_widget.clear_layout()
        if self.filter == self.all:
            scripts = [x for y in self.tool_data.keys() for x in self.tool_data[y].items()]
        else:
            scripts = [x for x in self.tool_data[self.filter].items()]
        scripts.sort(key=lambda x: x[0].lower())
        for name, value in scripts:
            button = QPushButton(name)
            button.setToolTip(value['tool_tip'])
            button.clicked.connect(partial(self.execute_script, value['script']))
            self.script_widget.add_widget(button)
        self.script_widget.layout().addStretch(1)

    @staticmethod
    def execute_script(script):
        exec(script)

class ToolCaddyDockable(QWidget):
    def __init__(self):
        super(ToolCaddyDockable, self).__init__()
        self.setLayout(VBoxLayout())
        self.layout().addWidget(ToolCaddy())
        self.layout().addStretch(1)


class ToolCaddyDM(dockable_widget.DockManager):
    def __init__(self):
        super(ToolCaddyDM, self).__init__()
        self.window_name = 'tool_caddy'
        self.mixin_cls = lambda: dockable_widget.MayaMixin(window_name=self.window_name,
                                                           main_widget_cls=ToolCaddyDockable, title='Tool Caddy')


if __name__ == '__main__':
    from importlib import reload
    from tools.ui import ad_widgets
    from tools.utils import tool_caddy

    reload(ad_widgets)
    reload(tool_caddy)

    if 'tool_caddy_tool' in globals():
        tool_caddy_tool.close()
    tool_caddy_tool = tool_caddy.ToolCaddy()
    tool_caddy_tool.show()
