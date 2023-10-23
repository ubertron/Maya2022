import pymel.core as pm
import inspect
import getpass
import logging

from maya import mel
from typing import List, Optional, Type
from functools import partial
from pathlib import Path

from robotools import icon_path
from robotools.maya_environment import get_environment_variable
from robotools.maya_scene import load_scene

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

_DEBUG_MODE: bool = False


class ShelfManager:
    TOP_LEVEL_SHELF: str = mel.eval('$tmpVar=$gShelfTopLevel')

    def __init__(self, name: str):
        self.name = name

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

    def create(self, select: bool = False):
        """
        Add the shelf to the ui
        :param select:
        """
        if self.name not in self.shelf_names:
            pm.shelfLayout(self.name, parent=self.TOP_LEVEL_SHELF)
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

    def add_shelf_button(self, label: str, icon: Path, command: str = '', overlay_label: Optional[str] = None,
                         overwrite: bool = True):
        """
        Add a button to the current shelf
        :param label: str
        :param icon: Path
        :param command: str
        :param overlay_label: str
        :param overwrite: bool
        """
        if label in self.current_button_labels and overwrite:
            self.delete_button(label=label)
        button = pm.shelfButton(label=label, image1=icon, parent=self.name, command=command)
        if overlay_label:
            button.setImageOverlayLabel(overlay_label)

    def add_separator(self):
        """
        Add a separator to the current shelf
        """
        pm.setParent(self.name)
        pm.separator(width=12, height=35, horizontal=False)

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


def setup_robotools_shelf():
    """
    Sets up the Robotools shelf
    """
    sm = ShelfManager('Robotools')
    sm.delete()
    sm.create(select=True)
    sm.delete_buttons()

    base_male_cmd = build_shelf_command(function=load_base_character, script='load_base_character("male")')
    base_female_cmd = build_shelf_command(function=load_base_character, script='load_base_character("female")')
    slice_cmd = build_shelf_command(function=slice_geometry, script='slice_geometry()')
    mirror_cmd = build_shelf_command(function=mirror_geometry, script='mirror_geometry()')

    sm.add_shelf_button(label='Robotools', icon=icon_path('robonobo_32.png'), command=message_script('Robotools!'))
    sm.add_separator()
    sm.add_shelf_button(label='Load Base Male', icon=icon_path('base_male.png'), command=base_male_cmd)
    sm.add_shelf_button(label='Load Base Female', icon=icon_path('base_female.png'), command=base_female_cmd)
    sm.add_separator()
    sm.add_shelf_button(label='Slice', icon=icon_path('slice.png'), command=slice_cmd)
    sm.add_shelf_button(label='Mirror', icon=icon_path('mirror.png'), command=mirror_cmd)


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


def load_base_character(gender: str):
    from robotools.maya_scene import load_scene
    from robotools import SCENES_FOLDER

    scene_path = SCENES_FOLDER.joinpath('base_mesh_male.mb' if gender == 'male' else 'base_mesh_female.mb')
    load_scene(scene_path)


def mirror_geometry():
    from robotools.maya_poly import mirror
    mirror()


def slice_geometry():
    from robotools.maya_poly import slice
    slice()
