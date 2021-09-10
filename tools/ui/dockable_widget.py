import pymel.core as pm

import inspect
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtGui, QtCore, QtWidgets

# Maya Bug introduced in 2018
# Global holds all widgets restored from maya preferences so that qt doesnt garbage collect
# them if they aren't currently visible (ex: in a docked tab that isn't the currently displayed tab).

restored_widgets = []


class DockManager(object):

    def __init__(self):
        """
        Must be over-ridden per UI.
        """

        # Main UI widget class for tool
        self.mixin_cls = None

        # Name used by my to reference UI
        self.window_name = None

    @classmethod
    def show(cls, debug=False):
        """
        Call to re-show or initiate the UI.
        :param bool debug: Set to True to re-initialize an existing UI.
        """

        # init dock manager
        instance = cls()

        # Test if tool is already open
        if pm.workspaceControl(instance.window_name + 'WorkspaceControl', ex=True):

            # Used to bypass saved dock preferences in maya workspaces. Useful for testing without restarting maya
            if debug:
                # Deletes existing UI
                pm.deleteUI(instance.window_name + 'WorkspaceControl')

                # Init new dock manager
                instance.__init__()

                # Rerun this show to create new UI. (the else below)
                instance.show()

            # Shows UI
            pm.workspaceControl(instance.window_name + 'WorkspaceControl', edit=True, restore=True)

        else:

            # Create mixin widget
            workspace_widget = instance.mixin_cls()

            # Get class name of widget
            class_name = instance.__class__.__name__

            # Get module name of widget
            module_name = inspect.getmodule(instance).__name__

            # Show widget and attach uiScript for restoring widget from maya close using class_name and module_name
            #  to define path to restore_from_close classmethod.
            # Import is in the uiScript to handle the case where it is not present in usersetup.py
            workspace_widget.show(dockable=True, uiScript='import {0}\n{0}.{1}.restore_from_close()'.format(module_name,
                                                                                                            class_name))

    @classmethod
    def restore_from_close(cls):
        """
        Called by Maya from the preferences when starting a new session to restore last session's ui.
        """

        # Init dock manager
        instance = cls()

        # Get the current maya control that the mixin widget should parent to
        restored_control = omui.MQtUtil.getCurrentParent()

        # Create mixin widget
        widget = instance.mixin_cls()

        # Find the widget created above as a maya control (aka a maya class)
        mixin_ptr = omui.MQtUtil.findControl(widget.objectName())

        # Hold on to pointer to widget so qt doesnt garbage collect it
        restored_widgets.append(widget)

        # Add mixin widget to container UI
        omui.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(restored_control))

    @staticmethod
    def close():
        print('DockManager is not closable as it restores itself')


class MayaMixin(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, window_name, main_widget_cls, title, **kwargs):
        super(MayaMixin, self).__init__(**kwargs)
        self.setObjectName(window_name)
        self._mainLayout = QtWidgets.QVBoxLayout()
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._mainLayout)
        self.mainWidget = main_widget_cls()
        self._mainLayout.addWidget(self.mainWidget)
        self.setWindowTitle(title)
