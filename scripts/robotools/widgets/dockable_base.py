import inspect

import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm

from PySide2 import QtWidgets
import shiboken2

mixinWindows = {}


class DockableBase(MayaQWidgetDockableMixin):
    """
    Convenience class for creating dockable Maya windows.
    """

    def __init__(self, controlName, **kwargs):
        super(DockableBase, self).__init__(**kwargs)
        self.setObjectName(controlName)

    def show(self, *args, **kwargs):
        """
        Show UI with generated uiScript argument
        """
        modulePath = inspect.getmodule(self).__name__
        className = self.__class__.__name__
        print(f"module path: {modulePath}\nclass name: {className}")
        super(DockableBase, self).show(dockable=True,
                                       uiScript="import {0}; {0}.{1}._restoreUI()".format(modulePath, className),
                                       **kwargs)

    @classmethod
    def _restoreUI(cls):
        """
        Internal method to restore the UI when Maya is opened.
        """
        # Create UI instance
        instance = cls()
        # Get the empty WorkspaceControl created by Maya
        workspaceControl = omui.MQtUtil.getCurrentParent()
        # Grab the pointer to our instance as a Maya object
        mixinPtr = omui.MQtUtil.findControl(instance.objectName())
        # Add our UI to the WorkspaceControl
        if pm.versions.current() > 20190000:
            omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(workspaceControl))
        else:
            omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(workspaceControl))
        # Store reference to UI
        global mixinWindows
        mixinWindows[instance.objectName()] = instance
