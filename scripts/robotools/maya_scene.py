import os
import pymel.core as pm
import logging

from typing import List
from enum import Enum
from pathlib import Path


def get_scene_name(include_extension: bool = False) -> str:
    """
    Get the name of the current scene
    :param include_extension:
    :return:
    """
    scene_name = os.path.basename(pm.system.sceneName())
    return scene_name if include_extension else os.path.splitext(scene_name)[0]


def get_scene_path() -> Path:
    """
    Get the full path of the scene
    :return:
    """
    return Path(pm.system.sceneName())


def new_scene():
    """
    Create a new scene in Maya
    """
    pm.system.newFile(force=True)


def load_scene(file_path: Path, force: bool = True):
    """
    Load a scene in Maya
    @param file_path:
    @param force:
    """
    assert file_path.exists(), 'Path does not exist.'
    pm.system.openFile(file_path.as_posix(), force=force)


def save_scene(force: bool = False) -> bool:
    """
    Perform a file save operation
    Returns false if there is no valid scene or if it is not possible to save the scene
    @param force: overwrite the path if possible
    @return:
    """
    scene_path = get_scene_path()

    if scene_path.as_posix() == '.':
        return False

    try:
        pm.system.saveFile(force=force)
        return True
    except RuntimeError as err:
        logging.error('Please check file out in Perforce prior to save.')
        return False


def create_reference(file_path: Path, force: bool = False) -> pm.system.FileReference:
    """
    Creates a reference in the Maya scene
    @param file_path: str path of the source file
    @param force: bool to create reference in a new scene
    @return: pm.system.FileReference
    """
    assert file_path.exists()
    if force:
        pm.system.newFile(force=True)
    return pm.system.createReference(file_path.as_posix())


class State:
    """Query and restore selection/component mode"""

    def __init__(self):
        self.component_mode = get_component_mode()
        self.selection = pm.ls(sl=True)
        if self.object_mode:
            self.object_selection = pm.ls(sl=True)
            self.component_selection = []
        else:
            self.component_selection = pm.ls(sl=True)
            set_component_mode(ComponentType.object)
            self.object_selection = pm.ls(sl=True)
            set_component_mode(self.component_mode)
            pm.hilite(self.object_selection)

    def restore(self):
        """
        Reset the Maya scene to the last state
        """
        if self.object_selection:
            pm.select(self.object_selection, noExpand=True)
            set_component_mode(self.component_mode)
        else:
            set_component_mode(ComponentType.object)
            pm.select(clear=True)
        if not self.object_mode:
            pm.select(self.component_selection)

    @property
    def object_mode(self) -> bool:
        return self.component_mode == ComponentType.object

    def remove_objects(self, objects: List[pm.nodetypes.Transform]) -> object:
        """
        Remove objects from current selection
        Sometimes necessary as pm.objExists check causes an exception
        @param objects:
        """
        for item in list(objects):
            if item in self.object_selection:
                self.object_selection.remove(item)


class ComponentType(Enum):
    vertex = 'vertex'
    edge = 'edge'
    face = 'face'
    object = 'object'
    vertex_face = 'vertex face'
    element = 'element'
    uv = 'uv'


def get_component_mode() -> ComponentType or None:
    """
    Determine which component mode Maya is currently in
    @return: ComponentType or None
    """
    if pm.selectMode(query=True, object=True):
        return ComponentType.object
    elif pm.selectType(query=True, vertex=True):
        return ComponentType.vertex
    elif pm.selectType(query=True, edge=True):
        return ComponentType.edge
    elif pm.selectType(query=True, facet=True):
        return ComponentType.face
    elif pm.selectType(query=True, polymeshUV=True):
        return ComponentType.uv
    else:
        return None


def set_component_mode(component_type: ComponentType = ComponentType.object):
    """
    Set the current Maya component mode
    @param component_type: ComponentType
    """
    if component_type == ComponentType.object:
        pm.selectMode(object=True)
    else:
        pm.selectMode(component=True)
        if component_type == ComponentType.vertex:
            pm.selectType(vertex=True)
        elif component_type == ComponentType.edge:
            pm.selectType(edge=True)
        elif component_type == ComponentType.face:
            pm.selectType(facet=True)
        elif component_type == ComponentType.uv:
            pm.selectType(polymeshUV=True)
        else:
            pm.warning('Unknown component type')


def create_group_node(name: str, overwrite: bool = False) -> pm.nodetypes.Transform:
    """
    Create an empty group node DAG object
    @param name:
    @param overwrite:
    @return:
    """
    if pm.objExists(name) and overwrite:
        pm.delete(name)
    group_node = pm.group(name=name, empty=True)
    return group_node


def query_unsaved_changes() -> bool:
    """
    Returns True if there are unsaved changes in the current scene
    @return: bool
    """
    from maya import cmds
    return cmds.file(query=True, modified=True)


def get_top_level_transforms() -> List[pm.nodetypes.Transform]:
    """
    :@return: Finds transforms that are children of the world
    """
    return [x for x in pm.ls(transforms=True) if not pm.listRelatives(x, parent=True)]
