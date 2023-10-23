from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QPushButton, QColorDialog, QSizePolicy

from core.widgets.layouts import HBoxLayout


class SwatchMultiButton(QWidget):
    def __init__(self, size, color=(1., 0., 0.), parent=None):
        super(SwatchMultiButton, self).__init__(parent=parent)
        self.size = size
        self.rgb_int_255 = tuple([int(x * 255) for x in color])
        self.setLayout(HBoxLayout(0))
        self.color_picker = QPushButton()
        self.color_picker.setFixedSize(size, size)
        self.color_picker.clicked.connect(self.swatch_button_clicked)
        self.color_picker.setStyleSheet(f'background-color: rgb{str(self.rgb_int_255)}')
        self.layout().addWidget(self.color_picker)

    def swatch_button_clicked(self):
        default = QColor()
        default.setRgb(*self.rgb_int_255)
        col = QColorDialog.getColor(default)
        if col.isValid():
            self.rgb_int_255 = self.hex_to_rgb(col.name())
            self.color_picker.setStyleSheet('background-color: {}'.format(col.name()))

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def add_button(self, label, event):
        button = QPushButton(label)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setFixedHeight(self.size)
        button.clicked.connect(event)
        self.layout().addWidget(button)
