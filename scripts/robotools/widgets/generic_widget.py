from PySide2.QtWidgets import QWidget, QSizePolicy

from robotools.widgets.layouts import VBoxLayout


class GenericWidget(QWidget):
    def __init__(self, parent=None):
        super(GenericWidget, self).__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setLayout(VBoxLayout(2))

    def add_widget(self, widget):
        self.layout().addWidget(widget)

    def replace_layout(self, layout):
        QWidget().setLayout(self.layout())
        self.setLayout(layout)

    def clear_layout(self, layout=None):
        if not layout:
            layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())
