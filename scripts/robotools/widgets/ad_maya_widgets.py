#! /usr/bin/env python

import os
import platform

from PySide2.QtCore import Qt, QRegExp, QSize
from PySide2.QtWidgets import QHBoxLayout, QPushButton, \
    QSizePolicy, QVBoxLayout, QWidget, QLabel, QTextEdit, \
    QColorDialog
from PySide2.QtGui import QColor, QPixmap
from maya.OpenMayaUI import MQtUtil
from maya import cmds
from shiboken2 import wrapInstance
from robotools.widgets.ad_dockable_base import ADDockableBase


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
        self.push_buttons = []
        self.widgets = []

    def expand_ui(self, value=True):
        """Set this to True to expand the contents to fill the container"""
        policy = QSizePolicy.Expanding if value else QSizePolicy.Maximum
        widget_types = [QPushButton, QLabel, QTextEdit]
        reg_exp = QRegExp(r'.*')
        for widget in [item for sublist in [self.findChildren(
                t, reg_exp) for t in widget_types] for item in sublist]:
            widget.setSizePolicy(policy, policy)

    def add_push_button(self, label, event):
        new_button = QPushButton(label)
        new_button.clicked.connect(event)
        self.push_buttons.append(new_button)
        self.layout().addWidget(new_button)

    @property
    def push_buttons_size(self):
        width = sum(x.sizeHint().width() for x in self.push_buttons)
        height = sum(x.sizeHint().height() for x in self.push_buttons)
        return QSize(width, height)

    def add_widget(self, widget):
        self.widgets.append(widget)
        self.layout().addWidget(widget)

    @property
    def widgets_size(self):
        width = sum(x.sizeHint().width() for x in self.widgets)
        height = sum(x.sizeHint().height() for x in self.widgets)
        return QSize(width, height)

    def replace_layout(self, layout):
        QWidget().setLayout(self.layout())
        self.setLayout(layout)

    def clear_layout(self, layout=None):
        if not layout:
            layout = self.layout()
            self.widgets = []
            self.push_buttons = []
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())


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
        for widget in [item for sublist in [self.findChildren(
                t, reg_exp) for t in widget_types] for item in sublist]:
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
    def __init__(self, margin=2):
        super(HBoxLayout, self).__init__()
        self.setContentsMargins(margin, margin, margin, margin)
        self.setMargin(margin)
        self.setSpacing(margin)


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


class ColorPickerButton(QWidget):
    def __init__(self, label, size, event, default_color=(255, 0, 0), parent=None):
        super(ColorPickerButton, self).__init__(parent=parent)
        self.color = default_color
        self.setLayout(HBoxLayout(0))
        event_button = QPushButton(label)
        event_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        event_button.setFixedHeight(size)
        event_button.clicked.connect(event)
        self.color_picker = QPushButton()
        self.color_picker.setFixedSize(size, size)
        self.color_picker.clicked.connect(self.swatch_button_clicked)
        rgb = str(default_color)
        self.color_picker.setStyleSheet(f'background-color: rgb{rgb};')
        self.layout().addWidget(event_button)
        self.layout().addWidget(self.color_picker)

    def swatch_button_clicked(self):
        default = QColor()
        default.setRgb(*self.color)
        col = QColorDialog.getColor(default)
        if col.isValid():
            self.color = self.hex_to_rgb(col.name())
            self.color_picker.setStyleSheet('background-color: {}'.format(col.name()))

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class SwatchMultiButton(QWidget):
    def __init__(self, size, color=(1., 0., 0.), parent=None):
        super(SwatchMultiButton, self).__init__(parent=parent)
        self.size = size
        self.rgb_int_255 = tuple([int(x * 255) for x in color])
        self.setLayout(HBoxLayout(0))
        self.color_picker = QPushButton()
        self.color_picker.setFixedSize(size, size)
        self.color_picker.clicked.connect(self.swatch_button_clicked)
        self.color_picker.setStyleSheet(f'background-color: rgb{str(self.rgb_int_255)}')
        self.layout().addWidget(self.color_picker)

    def swatch_button_clicked(self):
        default = QColor()
        default.setRgb(*self.rgb_int_255)
        col = QColorDialog.getColor(default)
        if col.isValid():
            self.rgb_int_255 = self.hex_to_rgb(col.name())
            self.color_picker.setStyleSheet('background-color: {}'.format(col.name()))

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def add_button(self, label, event):
        button = QPushButton(label)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        button.setFixedHeight(self.size)
        button.clicked.connect(event)
        self.layout().addWidget(button)


class IconButton(QPushButton):
    def __init__(self, label, icon_path, size=24):
        super(IconButton, self).__init__()
        if os.path.isfile(icon_path):
            self.setFixedSize(QSize(size, size))
            self.setIcon(QPixmap(icon_path))
            self.setToolTip(label)
        else:
            self.setMaximumHeight(size)
            self.setText(label)
