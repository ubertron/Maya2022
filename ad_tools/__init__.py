import os

ICON_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "icons"))
IMAGE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "images"))


def icon_path(icon_file_name):
    return os.path.join(ICON_DIR, icon_file_name)


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
