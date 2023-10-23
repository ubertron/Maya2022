from enum import Enum, auto, unique


class FileExtension(Enum):
    jpg = ".jpg"
    fbx = ".fbx"
    json = ".json"
    mb = ".mb"
    ma = ".ma"
    png = ".png"
    psd = ".psd"
    py = ".py"
    substance = ".substance"
    tga = ".tga"
    uasset = ".uasset"
    ztool = ".ztool"


@unique
class Alignment(Enum):
    horizontal = auto()
    vertical = auto()


@unique
class SoftwarePlatform(Enum):
    Houdini = auto()
    Maya = auto()
    Photoshop = auto()
    Standalone = auto()
    Substance = auto()
    Unreal = auto()


@unique
class Gender(Enum):
    male = auto()
    female = auto()
    other = auto()


@unique
class Axis(Enum):
    x = auto()
    y = auto()
    z = auto()
