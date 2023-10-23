import platform

from maya import OpenMayaUI
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance

from core.widgets.generic_widget import GenericWidget
from core import DARWIN_STR

MAYA_MAIN_WINDOW = wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QMainWindow)


class MayaWidget(GenericWidget):
    def __init__(self, name: str, parent=None):
        super(MayaWidget, self).__init__(name=name, parent=parent)
        self.mayaMainWindow = MAYA_MAIN_WINDOW
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(Qt.Tool if platform.system() == DARWIN_STR else Qt.Window)
