from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QPushButton, QSizePolicy, QColorDialog

from core.widgets.layouts import HBoxLayout


class ColorPickerButton(QWidget):
    def __init__(self, label, size, event, default_color=(255, 0, 0), parent=None):
        super(ColorPickerButton, self).__init__(parent=parent)
        self.color = default_color
        self.setLayout(HBoxLayout(0))
        event_button = QPushButton(label)
        event_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        event_button.setFixedHeight(size)
        event_button.clicked.connect(event)
        self.color_picker = QPushButton()
        self.color_picker.setFixedSize(size, size)
        self.color_picker.clicked.connect(self.swatch_button_clicked)
        rgb = str(default_color)
        self.color_picker.setStyleSheet(f'background-color: rgb{rgb};')
        self.layout().addWidget(event_button)
        self.layout().addWidget(self.color_picker)

    def swatch_button_clicked(self):
        default = QColor()
        default.setRgb(*self.color)
        col = QColorDialog.getColor(default)
        if col.isValid():
            self.color = self.hex_to_rgb(col.name())
            self.color_picker.setStyleSheet('background-color: {}'.format(col.name()))

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
