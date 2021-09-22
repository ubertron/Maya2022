#! /usr/bin/env python

import os
import platform

import pymel.core as pm
from PySide2.QtCore import Signal, Qt, QRegExp
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, \
    QWidget, QDialog, QLabel, QTextEdit, QWidgetItem, QLayout, QGridLayout
from maya.OpenMayaUI import MQtUtil
from maya import cmds
from shiboken2 import wrapInstance, getCppPointer
from ad_tools.ui.ad_dockable_base import ADDockableBase


def maya_main_window():
    main_window_ptr = MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class ADMayaWidget(QWidget):
    def __init__(self, window_name, v_layout=True, parent=maya_main_window()):
        super(ADMayaWidget, self).__init__(parent)
        self.setWindowTitle(window_name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        margin_size = 2
        layout = VBoxLayout(margin_size) if v_layout else HBoxLayout(margin_size)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Tool if platform.system() == 'Darwin' else Qt.Window)

    def expand_ui(self, value=True):
        """Set this to True to expand the contents to fill the container"""
        policy = QSizePolicy.Expanding if value else QSizePolicy.Maximum
        widget_types = [QPushButton, QLabel, QTextEdit]
        reg_exp = QRegExp(r'.*')
        for widget in [item for sublist in [self.findChildren(t, reg_exp) for t in widget_types] for item in sublist]:
            widget.setSizePolicy(policy, policy)

    def init_button(self, label, event):
        new_button = QPushButton(label)
        new_button.clicked.connect(event)
        self.ui.addWidget(new_button)

    def add_widget(self, widget):
        self.layout().addWidget(widget)

    def replace_layout(self, layout):
        QWidget().setLayout(self.layout())
        self.setLayout(layout)


class ADMayaDockableWidget(ADDockableBase, QWidget):
    def __init__(self, control_name, window_name, v_layout=True):
        super(ADMayaDockableWidget, self).__init__(controlName=control_name)
        self.setWindowTitle(window_name)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        margin_size = 2
        layout = VBoxLayout(margin_size) if v_layout else HBoxLayout(margin_size)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Tool if platform.system() == 'Darwin' else Qt.Window)

    def expand_ui(self, value=True):
        """Set this to True to expand the contents to fill the container"""
        policy = QSizePolicy.Expanding if value else QSizePolicy.Maximum
        widget_types = [QPushButton, QLabel, QTextEdit]
        reg_exp = QRegExp(r'.*')
        for widget in [item for sublist in [self.findChildren(t, reg_exp) for t in widget_types] for item in sublist]:
            widget.setSizePolicy(policy, policy)

    def init_button(self, label, event):
        new_button = QPushButton(label)
        new_button.clicked.connect(event)
        self.ui.addWidget(new_button)

    def add_widget(self, widget):
        self.layout().addWidget(widget)

    def replace_layout(self, layout):
        QWidget().setLayout(self.layout())
        self.setLayout(layout)

class VBoxLayout(QVBoxLayout):
    def __init__(self, margin=2):
        super(VBoxLayout, self).__init__()
        self.setContentsMargins(margin, margin, margin, margin)
        self.setMargin(margin)
        self.setSpacing(margin)

class HBoxLayout(QHBoxLayout):
    def __init__(self, margin):
        super(HBoxLayout, self).__init__()
        self.setContentsMargins(margin, margin, margin, margin)


class ADWidget(QWidget):
    def __init__(self, parent=None):
        super(ADWidget, self).__init__(parent=parent)
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


def delete_existing_workspace_control(token):
    workspace_control_name = f"{token}WorkspaceControl"
    if cmds.workspaceControl(workspace_control_name, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, close=True)
        cmds.deleteUI(workspace_control_name, control=True)
