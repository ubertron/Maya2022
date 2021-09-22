from importlib import reload
from PySide2.QtWidgets import QPushButton, QDialog, QVBoxLayout

from ad_tools.ui.ad_dockable_widget import ADDockableBase


class MyDockableWindow(ADDockableBase, QDialog):
    control_name = "MyWindow"
    window_title = "My Window"

    def __init__(self):
        super(MyDockableWindow, self).__init__(controlName=self.control_name)
        self.setWindowTitle(self.window_title)

        self.pushButton = QPushButton("Push me or else!", parent=self)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.pushButton)
