import json
import os

from PySide2.QtWidgets import QComboBox, QLabel, QWidget, QPushButton
from PySide2.QtCore import QSettings
from ad_tools.ui.ad_maya_widgets import ADWidget, ADMayaDockableWidget
from ad_tools.ui.ad_dockable_base import ADDockableBase
from functools import partial


class ToolCaddy(ADMayaDockableWidget):
    control_name = 'ToolCaddy'
    window_name = 'Tool Caddy'
    JSON_PATH = os.path.join(os.path.dirname(__file__), 'tool_caddy.json')
    all = 'All'

    def __init__(self):
        super(ToolCaddy, self).__init__(self.control_name, self.window_name)
        with open(self.JSON_PATH) as f:
            self.tool_data = json.load(f)
        self.settings = QSettings('robosoft', 'tool_caddy')
        self.filter = self.settings.value('filter', self.all)
        self.combo_box = QComboBox()
        self.button_widget = ADWidget()
        self.script_widget = ADWidget()
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


if __name__ == '__main__':
    from ad_tools.utils import tool_caddy

    tools = tool_caddy.ToolCaddy()
    tools.show()
