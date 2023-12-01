import pymel.core as pm
import platform

from pathlib import Path

from robotools import icon_path, PROJECT_ROOT
from robotools.utils.shelf_manager import ShelfManager, message_script, build_shelf_command
from robotools.utils import hotkey_utils

ROBOTOOLS_TITLE: str = 'RobotoolsHotkeys'
ROBOTOOLS_HOTKEYS: Path = PROJECT_ROOT.joinpath('startup', '{}.mhk'.format(ROBOTOOLS_TITLE))
ROBOTOOLS_SHELF_NAME: str = 'Robotools'
ROBOTOOLS_SHELF_VERSION: str = '0.2'
ROBOTOOLS_SHELF_PLUG_IN: str = 'robotools_shelf'
ROBOTOOLS_SHELF_PLUG_IN_PATH: Path = Path(pm.pluginInfo(ROBOTOOLS_SHELF_PLUG_IN, query=True, path=True))
DARWIN: str = 'Darwin'


def setup_robotools_shelf():
    """
    Sets up the Robotools shelf
    """
    sm = ShelfManager(ROBOTOOLS_SHELF_NAME)
    sm.delete()
    sm.create(select=False)
    sm.delete_buttons()

    version_info = f'Robotools Shelf Version {ROBOTOOLS_SHELF_VERSION}: {ROBOTOOLS_SHELF_PLUG_IN_PATH.as_posix()}'
    robonobo_icon = icon_path('robonobo_32.png')
    script_icon = icon_path('script.png')
    import_base_male = 'from robotools.character_utils import import_base_character\nimport_base_character("male")'
    load_base_male = 'from robotools.character_utils import load_base_character\nload_base_character("male")'
    import_base_female = 'from robotools.character_utils import import_base_character\nimport_base_character("female")'
    load_base_female = 'from robotools.character_utils import load_base_character\nload_base_character("female")'
    slice_geometry = 'from robotools.geometry_utils import slice_geometry\nslice_geometry()'
    mirror = 'from robotools.geometry_utils import mirror_geometry\nmirror_geometry()'
    merge = 'from robotools.geometry_utils import merge_vertices\nmerge_vertices()'
    quadrangulate = 'from robotools.geometry_utils import quadrangulate\nquadrangulate()'
    update_hotkeys_cmd = build_shelf_command(function=update_hotkeys, script='update_hotkeys()')

    sm.add_shelf_button(label=ROBOTOOLS_SHELF_NAME, icon=robonobo_icon, command=message_script(version_info))
    sm.add_shelf_button(label='Update Hotkeys', icon=script_icon, command=update_hotkeys_cmd,
                        overlay_label='Htkys')
    sm.add_separator()
    sm.add_shelf_button(label='Import Base Male', icon=icon_path('base_male.png'), command=import_base_male)
    sm.add_shelf_button(label='Load Base Male', icon=script_icon, command=load_base_male, overlay_label='loadM')
    sm.add_shelf_button(label='Import Base Female', icon=icon_path('base_female.png'), command=import_base_female)
    sm.add_shelf_button(label='Load Base Female', icon=script_icon, command=load_base_female, overlay_label='loadF')
    sm.add_separator()
    sm.add_shelf_button(label='Slice', icon=icon_path('slice.png'), command=slice_geometry)
    sm.add_shelf_button(label='Mirror', icon=icon_path('mirror.png'), command=mirror)
    sm.add_shelf_button(label='Merge Vertices', icon=script_icon, overlay_label='merge', command=merge)
    sm.add_shelf_button(label='Quadrangulate', icon=script_icon, overlay_label='quad', command=quadrangulate)


def delete_robotools_shelf():
    """
    Get rid of the shelf
    """
    ShelfManager('Robotools').delete()


class RobotoolsHotkeyManager(hotkey_utils.HotkeyManager):
    def __init__(self):
        super(RobotoolsHotkeyManager, self).__init__(name=ROBOTOOLS_TITLE, path=ROBOTOOLS_HOTKEYS)

    def init_hotkeys(self):
        """
        Set up the hotkeys
        """
        is_mac: bool = platform.system() == DARWIN
        is_pc: bool = not is_mac

        self.set_hotkey('hotkeyPrefs', annotation='Hotkey Editor', mel_command='HotkeyPreferencesWindow',
                        key='H', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('appendToPoly', annotation='Append To Poly', mel_command='AppendToPolygonTool',
                        key='A', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('createPoly', annotation='Create Polygon Tool', mel_command='CreatePolygonTool',
                        key='C', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('combine', annotation='Combine', mel_command='CombinePolygons',
                        key='A', cmd=is_mac, ctrl=is_pc, alt=True, overwrite=True)
        self.set_hotkey('mergeVertices', annotation='Merge Vertices', mel_command='PolyMergeVertices',
                        key='W', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('toggleGrid', annotation='Toggle Grid', mel_command='ToggleGrid',
                        key=';', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('selectEdgeLoop', annotation='Select Edge Loop', mel_command='SelectEdgeLoopSp',
                        key=']', cmd=is_mac, ctrl=is_pc, overwrite=True)
        self.set_hotkey('selectEdgeRing', annotation='Select Edge Ring', mel_command='SelectEdgeRingSp',
                        key='[', cmd=is_mac, ctrl=is_pc, overwrite=True)


def update_hotkeys():
    """
    Script deletes the hotkey preferences file and sets up a new one from script
    """
    import logging
    from importlib import reload
    from robotools import robotools_utils

    logging.info('>>>> Updating Robotools Hotkeys')
    reload(robotools_utils)

    if robotools_utils.ROBOTOOLS_HOTKEYS.exists():
        os.remove(robotools_utils.ROBOTOOLS_HOTKEYS.as_posix())

    robotools_utils.RobotoolsHotkeyManager().init_hotkeys()
