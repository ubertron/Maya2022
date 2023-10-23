# https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=Maya_SDK_Maya_Python_API_Writing_Workspace_controls_html
# https://gist.github.com/cerina/80d4b99721a29f63e3b30cce5ed3cc28

from shiboken2 import wrapInstance
from PySide2 import QtCore, QtWidgets
import pymel.core as pm
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from robotools.widgets import MAYA_MAIN_WINDOW


def delete_workspace_control(control):
    if pm.workspaceControl(control, q=True, exists=True):
        pm.workspaceControl(control, e=True, close=True)
        pm.deleteUI(control, control=True)


class MyDockableWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    TOOL_NAME = 'My Dockable UI'

    def __init__(self, parent=None):
        delete_workspace_control(self.TOOL_NAME + 'WorkspaceControl')

        super(self.__class__, self).__init__(parent=parent)
        self.mayaMainWindow = MAYA_MAIN_WINDOW
        self.setObjectName(self.__class__.TOOL_NAME)

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(self.TOOL_NAME)
        self.resize(200, 200)

        # Set the layout of the window.
        self.setLayout(QtWidgets.QVBoxLayout())

        # Add button widget examples.
        self.populate_buttons()

    def populate_buttons(self):
        button = QtWidgets.QPushButton('Create Cube')
        button.clicked.connect(pm.polyCube)
        self.layout().addWidget(button)

        button = QtWidgets.QPushButton('Create Sphere')
        button.clicked.connect(pm.polySphere)
        self.layout().addWidget(button)

        # Add a vertical spacer to make the UI look neater.
        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout().addItem(vertical_spacer)


my_win = MyDockableWindow()
my_win.show(dockable=True)
