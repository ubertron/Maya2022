from enum import Enum, auto, unique


@unique
class Gender(Enum):
    male = auto()
    female = auto()
    other = auto()


class Axis(Enum):
    def __init__(self):
        pass

    x = "x"
    y = "y"
    z = "z"