import pymel.core as pm
import inspect
import logging

from maya import mel
from typing import List, Optional, Type, Tuple
from pathlib import Path
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QFrame

from robotools import icon_path

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

_DEBUG_MODE: bool = False


class ShelfManager:
    TOP_LEVEL_SHELF: str = mel.eval('$tmpVar=$gShelfTopLevel')

    def __init__(self, name: str, spacing: int = 4):
        self.name = name
        self._spacing = spacing

    @property
    def shelf_names(self) -> List[str]:
        return pm.tabLayout(self.TOP_LEVEL_SHELF, query=True, childArray=True)

    @property
    def current_button_labels(self) -> List[str]:
        return [pm.shelfButton(x, query=True, label=True) for x in self.current_buttons]

    @property
    def current_buttons(self) -> List[str]:
        shelf_contents = pm.shelfLayout(self.name, query=True, childArray=True)
        return [] if shelf_contents is None else [x for x in shelf_contents if 'shelfButton' in x]

    @property
    def tab_index(self) -> int or None:
        return self.shelf_names.index(self.name) + 1 if self.name in self.shelf_names else None

    @property
    def exists(self):
        return pm.shelfLayout(self.name, query=True, exists=True)

    @property
    def spacing(self) -> int or None:
        return pm.shelfLayout(self.name, query=True, spacing=True) if self.exists else None

    @spacing.setter
    def spacing(self, value: int):
        if self.exists:
            pm.shelfLayout(self.name, edit=True, spacing=value)

    def create(self, select: bool = False):
        """
        Add the shelf to the ui
        :param select:
        """
        if self.name not in self.shelf_names:
            pm.shelfLayout(self.name, parent=self.TOP_LEVEL_SHELF)
            self.spacing = self._spacing
            if select:
                self.select_tab_index()

    def delete(self):
        """
        Remove the shelf from the ui
        """
        if self.name in self.shelf_names:
            pm.deleteUI(self.name)

    def select_tab_index(self, tab_index: Optional[int] = None):
        """
        Set the currently selected shelf tab
        :param tab_index:
        """
        if tab_index is not None:
            assert tab_index <= len(self.shelf_names), 'Invalid index'
        pm.shelfTabLayout(self.TOP_LEVEL_SHELF, edit=True, selectTabIndex=tab_index if tab_index else self.tab_index)

    def select_tab_name(self, name: Optional[str] = None):
        """
        Select the current tab by name
        :param name: str
        """
        if name is not None:
            assert name in self.shelf_names, 'Invalid shelf name'
        pm.shelfTabLayout(self.TOP_LEVEL_SHELF, edit=True, selectTab=name if name else self.name)

    def add_shelf_button(self, label: str, icon: Optional[Path] = None, command: str = '',
                         overlay_label: Optional[str] = None,  overwrite: bool = True):
        """
        Add a button to the current shelf
        :param label: str
        :param icon: Path or None
        :param command: str
        :param overlay_label: str
        :param overwrite: bool
        """
        if label in self.current_button_labels and overwrite:
            self.delete_button(label=label)

        icon = icon if icon else icon_path('script.png')
        button = pm.shelfButton(label=label, image1=icon, parent=self.name, command=command,
                                overlayLabelBackColor=(0, 0, 0, 0))
        if overlay_label:
            button.setImageOverlayLabel(overlay_label)

    def add_separator(self, color: Tuple[float] = (0.9, 0.9, 0.9)):
        """
        Add a separator to the current shelf
        @param color: tuple
        """
        pm.setParent(self.name)
        separator = pm.separator(width=12, height=35, horizontal=False)
        qt_sep: QFrame = pm.windows.toQtObject(separator)
        qt_sep.setFixedWidth(1)
        rgb = [str(int(color[i] * 255)) for i in range(3)]
        rgb_string = f'rgb({", ".join(rgb)})'
        style_string = f'border-width: 1; border-style: solid; border-color: {rgb_string};'
        qt_sep.setStyleSheet(style_string)

    def add_label(self, text: str, bold: bool = False):
        """
        Add a text to the current shelf
        """
        pm.setParent(self.name)
        pm.text(label=f'<b>{text}</b>' if bold else text, width=len(text) * 7, align='center')

    def delete_button(self, label: str):
        """
        Delete a button by label
        :param label:
        """
        button = next((x for x in self.current_buttons if pm.shelfButton(x, query=True, label=True) == label), None)
        if button:
            pm.deleteUI(button)

    def delete_buttons(self):
        """
        Delete all buttons in shelf
        """
        for button in self.buttons:
            pm.deleteUI(button)

    @property
    def buttons(self) -> List[str]:
        buttons = pm.shelfLayout(self.name, query=True, childArray=True)
        return buttons if buttons is not None else []


def build_shelf_command(function: Type, script: str, imports: Optional[str] = None) -> str:
    """
    Creates a text script incorporating a function, a function call and an optional import header
    The command can be executed by Maya shelf buttons
    :param function:
    :param script:
    :param imports:
    :return:
    """
    import_string = f'{imports}\n\n' if imports else ''
    return f'{import_string}{inspect.getsource(function)}\n\n{script}'


def message_script(text: str) -> str:
    """
    Creates a script which launches an in-view message
    @param text:
    @return:
    """
    return f'import pymel.core as pm\npm.inViewMessage(assistMessage="{text}", fade=True, pos="midCenter")'


def launch_tool_caddy():
    from robotools.maya_tools import launch_utility
    from robotools.utils import tool_caddy

    launch_utility(module=tool_caddy, utility_class=tool_caddy.ToolCaddy)
