import pymel.core as pm

from robotools.maya_scene import load_scene, import_model
from robotools import SCENES_FOLDER, MODELS_FOLDER


BASE_MESH_MALE = 'base_mesh_male.fbx'
BASE_MESH_FEMALE = 'base_mesh_female.fbx'


def import_base_character(gender: str):
    """
    Import a base character
    @param gender:
    """
    import_path = MODELS_FOLDER.joinpath(BASE_MESH_MALE if gender == 'male' else BASE_MESH_FEMALE)
    result = import_model(import_path=import_path)
    transform = next(x for x in result if type(x) is pm.nodetypes.Transform)
    pm.select(transform)
    pm.viewFit()


def load_base_character(gender: str):
    """
    Load a base character scene
    @param gender:
    """
    scene_path = SCENES_FOLDER.joinpath(BASE_MESH_MALE if gender == 'male' else BASE_MESH_FEMALE)
    result = load_scene(scene_path)
    transform = next(x for x in result if type(x) is pm.nodetypes.Transform)
    pm.select(transform)
    pm.viewFit()
