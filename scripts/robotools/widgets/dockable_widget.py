# https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=Maya_SDK_Maya_Python_API_Writing_Workspace_controls_html
# https://gist.github.com/cerina/80d4b99721a29f63e3b30cce5ed3cc28

import pymel.core as pm

from PySide2 import QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from robotools.widgets.maya_widget import MayaWidget


def delete_workspace_control(control):
    """
    Ensures that a workspace control is deleted to avoid conflict issues when creating
    @param control:
    """
    if pm.workspaceControl(control, q=True, exists=True):
        pm.workspaceControl(control, e=True, close=True)
        pm.deleteUI(control, control=True)


class DockableWidget(MayaQWidgetDockableMixin, MayaWidget):
    def __init__(self, name: str, parent=None):
        """
        Creates a dockable workspace control
        Inherit from this class to build tools
        @param name:
        @param parent:
        """
        delete_workspace_control(f'{name}WorkspaceControl')
        super(DockableWidget, self).__init__(name=name, parent=parent)


def demo():
    from robotools.widgets.dockable_widget import DockableWidget
    from PySide2.QtWidgets import QSizePolicy

    class TestTool(DockableWidget):
        def __init__(self, name: str):
            super(TestTool, self).__init__(name=name)
            self.add_button('Button')
            self.add_label('Label')

    test_tool = TestTool(name='Test Tool')
    test_tool.show(dockable=True)
