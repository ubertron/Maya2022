import os

ICON_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "icons"))


def icon_path(icon_file_name):
    return os.path.join(ICON_PATH, icon_file_name)


class Axis:
    x = "x"
    y = "y"
    z = "z"