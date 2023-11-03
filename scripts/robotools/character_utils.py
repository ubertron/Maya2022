import pymel.core as pm

from robotools.maya_scene import load_scene, import_model
from core.common_enums import FileExtension, Gender
from robotools import SCENES_FOLDER, MODELS_FOLDER


BASE_MESH_MALE = 'base_mesh_male'
BASE_MESH_FEMALE = 'base_mesh_female'


def import_base_character(gender: str):
    """
    Import a base character
    @param gender:
    """
    file_name = f'{BASE_MESH_MALE if gender == Gender.male.name else BASE_MESH_FEMALE}{FileExtension.fbx.value}'
    import_path = MODELS_FOLDER.joinpath(file_name)
    result = import_model(import_path=import_path)
    transform = next(x for x in result if type(x) is pm.nodetypes.Transform)
    pm.select(transform)
    pm.viewFit()


def load_base_character(gender: str, latest: bool = True):
    """
    Load a base character scene
    @param gender:
    @param latest:
    """
    scene_name = BASE_MESH_MALE if gender == Gender.male.name else BASE_MESH_FEMALE

    if latest:
        # find all the scenes
        scenes = SCENES_FOLDER.glob(f'{scene_name}*')
        # discount the non-versioned file
        scenes = [x for x in scenes if len(x.as_posix().split('.')) == 3]
        # find the highest version
        scenes.sort(key=lambda x: x.stem.split('.')[1])
        scene_path = scenes[-1]
    else:
        scene_path = SCENES_FOLDER.joinpath(f'{scene_name}{FileExtension.mb.value}')

    result = load_scene(scene_path)
    transform = next(x for x in result if type(x) is pm.nodetypes.Transform)
    pm.select(transform)
    pm.viewFit()
