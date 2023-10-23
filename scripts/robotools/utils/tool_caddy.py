import json
import os
from functools import partial

from PySide2.QtCore import QSettings
from PySide2.QtWidgets import QComboBox, QLabel, QPushButton, QSizePolicy

from robotools import icon_path
from robotools.widgets.maya_widgets import MayaDockableWidget, IconButton
from robotools.widgets.generic_widget import GenericWidget


class ToolCaddy(MayaDockableWidget):
    control_name = 'ToolCaddy'
    window_name = 'Tool Caddy'
    JSON_PATH = os.path.join(os.path.dirname(__file__), 'tool_caddy.json')
    all = 'All'

    def __init__(self):
        super(ToolCaddy, self).__init__(self.control_name, self.window_name)
        self.settings = QSettings('robotools', 'tool_caddy')
        self.filter = self.settings.value('filter', self.all)
        button_bar = GenericWidget()
        self.refresh_button = IconButton("Refresh Button", icon_path('refresh.png'), 24)
        button_bar.add_widget(self.refresh_button)
        button_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.combo_box = QComboBox()
        self.button_widget = GenericWidget()
        self.script_widget = GenericWidget()
        self.status_bar = QLabel('Ready')
        self.add_widget(button_bar)
        self.add_widget(self.combo_box)
        self.add_widget(self.script_widget)
        self.add_widget(self.status_bar)
        self.init_combo_box()
        self.refresh_button.clicked.connect(self.refresh_button_clicked)
        self.refresh_buttons()
        self.setMinimumWidth(320)

    @property
    def tool_data(self):
        with open(self.JSON_PATH) as f:
            return json.load(f)

    def init_combo_box(self):
        self.combo_box.clear()
        tool_keys = list(self.tool_data.keys())
        tool_keys.sort(key=lambda x: x.lower())
        self.combo_box.addItems([self.all] + tool_keys)
        self.combo_box.setCurrentText(self.filter)
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)

    def refresh_button_clicked(self):
        self.status_bar.setText('Refresh button clicked')
        self.refresh_buttons()

    def combo_box_changed(self):
        self.filter = self.combo_box.currentText()
        self.status_bar.setText(f'Filter changed to {self.filter}')
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


# if __name__ == '__main__':
#     from robotools.utils import tool_caddy
#
#     tools = tool_caddy.ToolCaddy()
#     tools.show()
