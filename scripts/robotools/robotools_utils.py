import pymel.core as pm

from pathlib import Path

from robotools import icon_path
from robotools.utils.shelf_manager import ShelfManager, message_script

ROBOTOOLS_SHELF_NAME: str = 'Robotools'
ROBOTOOLS_SHELF_VERSION = '0.2'
ROBOTOOLS_SHELF_PLUG_IN = 'robotools_shelf'
ROBOTOOLS_SHELF_PLUG_IN_PATH = Path(pm.pluginInfo(ROBOTOOLS_SHELF_PLUG_IN, query=True, path=True))


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

    sm.add_shelf_button(label=ROBOTOOLS_SHELF_NAME, icon=robonobo_icon, command=message_script(version_info))
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
