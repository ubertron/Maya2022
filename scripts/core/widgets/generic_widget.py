from PySide2 import QtWidgets

from core.widgets.layouts import VBoxLayout


class GenericWidget(QtWidgets.QWidget):
    def __init__(self, name: str, parent=None):
        super(GenericWidget, self).__init__(parent=parent)
        self.tool_name = name
        self.setWindowTitle(self.tool_name)
        self.setObjectName(self.tool_name)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.setLayout(VBoxLayout(2))

    def add_widget(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        self.layout().addWidget(widget)
        return widget

    def add_label(self, text: str) -> QtWidgets.QLabel:
        return self.add_widget(QtWidgets.QLabel(text))

    def add_button(self, text: str) -> QtWidgets.QPushButton:
        return self.add_widget(QtWidgets.QPushButton(text))

    def replace_layout(self, layout: QtWidgets.QLayout):
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
    app = QtWidgets.QApplication()
    tool = GenericWidget()
    tool.add_button('BUTTON')
    tool.resize(320, 120)
    tool.show()
    app.exec_()
