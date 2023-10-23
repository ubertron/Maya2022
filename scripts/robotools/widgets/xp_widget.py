
import platform

from PySide2.QtWidgets import QWidget, QLabel, QLayout, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide2.QtCore import Qt
from typing import Optional, Callable
from core.system_utils import is_using_maya_python
from core import DARWIN_STR
from core.common_enums import Alignment


class XPWidget(QWidget):
    ICON_SIZE: int = 16

    def __init__(self, title: str = None, alignment: Alignment = Alignment.vertical, margin: int = 0, spacing: int = 0,
                 parent: Optional[QWidget] = None):
        """
        Generic widget
        :param title: Optional[str]
        :param alignment: Alignment
        :param margin: int
        :param spacing: int
        :param parent: int
        """
        if is_using_maya_python() and parent is None:
            from robotools.widgets import MAYA_MAIN_WINDOW
            parent = MAYA_MAIN_WINDOW

        super(XPWidget, self).__init__(parent=parent)

        if is_using_maya_python():
            self.setWindowFlags(Qt.Tool if platform.system() == DARWIN_STR else Qt.Window)

        self.setWindowTitle(title)
        self.setLayout(QVBoxLayout() if alignment == alignment.vertical else QHBoxLayout())
        self.set_margin(margin)
        self.set_spacing(spacing)
        self.setStyleSheet("QToolTip {background-color: black; color: white;  border: black solid 1px}")

    def add_widget(self, widget: QWidget) -> QWidget:
        """
        Add a widget to the widget
        @param widget:
        @return:
        """
        self.layout().addWidget(widget)
        return widget

    def add_label(self, text: str = "") -> QLabel:
        """
        Add a label to the widget
        @param text:
        @return:
        """
        return self.add_widget(QLabel(text))

    def add_button(self, text: str, tool_tip: str = None, event: Optional[Callable] = None) -> QPushButton:
        """
        Add a QPushButton to the layout
        @param text: str
        @param tool_tip: str
        @param event: slot method
        @return: QPushbutton
        """
        button = QPushButton(text)
        button.setToolTip(tool_tip)
        if event:
            button.clicked.connect(event)
        return self.add_widget(button)

    def replace_layout(self, layout: QLayout):
        """
        Replace the widget layout with a new layout item
        :param layout:
        """
        QWidget().setLayout(self.layout())
        self.setLayout(layout)

    def clear_layout(self):
        """
        Remove all widgets from the current layout
        """
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def add_stretch(self):
        """
        Add a stretch item to the layout
        """
        self.layout().addStretch(True)

    def add_spacing(self, value: int):
        """
        Add spacing to the layout
        :param value: size of the spacing
        """
        self.layout().addSpacing(value)

    def set_margin(self, value: int):
        """
        Set widget margin
        :param value:
        """
        self.layout().setMargin(value)

    def set_spacing(self, value: int):
        """
        Set widget spacing
        :param value:
        """
        self.layout().setSpacing(value)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    xp_widget = XPWidget(title='My Test Widget', margin=4, spacing=4)

    for x in range(10):
        xp_widget.add_label(f'Label {x + 1}')

    xp_widget.resize(330, xp_widget.sizeHint().height())
    xp_widget.add_button('Clear', event=xp_widget.clear_layout)
    xp_widget.show()
    app.exec_()
