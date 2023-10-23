import os
from pathlib import Path

from robotools.maya_environment import get_environment_variable

ROBOTOOLS_ROOT: Path = Path(get_environment_variable('ROBOTOOLS_ROOT')[0])
ICON_DIR: Path = ROBOTOOLS_ROOT.joinpath('icons')
SCENES_FOLDER: Path = ROBOTOOLS_ROOT.joinpath('scenes')
IMAGE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "images"))


def icon_path(file_name: str) -> Path:
    return ICON_DIR.joinpath(file_name)


def maya_path(relative_path):
    return os.path.join(os.path.join(os.path.dirname(__file__)), relative_path)


def image_path(image_file_name):
    return os.path.join(IMAGE_DIR, image_file_name)


class DataType:
    float3 = "float3"
    string = "string"

    def __init__(self):
        pass


class NodeType:
    mesh = "mesh"
    surfaceShape = "surfaceShape"
    shape = "shape"
    transform = "transform"

    def __init__(self):
        pass


class TransformationType:
    def __init__(self):
        pass

    translation = "translation"
    rotation = "rotation"
    scale = "scale"


class ComponentType:
    vertex = "vertex"
    edge = "edge"
    face = "face"
    object = "object"
    vertex_face = "vertex face"
    element = "element"
    uv = "uv"

    def __init__(self):
        pass


class Axis:
    def __init__(self):
        pass

    x = "x"
    y = "y"
    z = "z"


class FileType:
    def __init__(self):
        pass

    png = "png"
