import os
from pathlib import Path

from robotools.maya_environment import get_environment_variable

ROBOTOOLS_ROOT: Path = Path(get_environment_variable('ROBOTOOLS_ROOT')[0])
ICON_DIR: Path = ROBOTOOLS_ROOT.joinpath('icons')
MODELS_FOLDER: Path = ROBOTOOLS_ROOT.joinpath('models')
SCENES_FOLDER: Path = ROBOTOOLS_ROOT.joinpath('scenes')
IMAGE_DIR = ROBOTOOLS_ROOT.joinpath('images')


def icon_path(file_name: str) -> Path:
    return ICON_DIR.joinpath(file_name)


def image_path(image_file_name):
    return os.path.join(IMAGE_DIR, image_file_name)
