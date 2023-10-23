from enum import Enum, auto, unique


@unique
class ComponentType:
    vertex = auto()
    edge = auto()
    face = auto()
    object = auto()
    vertex_face = auto()
    element = auto()
    uv = auto()


@unique
class TransformationType(Enum):
    translation = auto()
    rotation = auto()
    scale = auto()


@unique
class MayaDataType(Enum):
    float3 = auto()
    string = auto()


@unique
class MayaNodeType(Enum):
    mesh = auto()
    surfaceShape = auto()
    shape = auto()
    transform = auto()
