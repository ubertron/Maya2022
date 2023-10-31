import os
import sys

from pathlib import Path

ROBOTOOLS_ROOT: Path = Path(r'C:\Users\idavisan\Documents\Projects\Maya2022')
ICON_DIR: Path = ROBOTOOLS_ROOT.joinpath('icons')
MODELS_FOLDER: Path = ROBOTOOLS_ROOT.joinpath('models')
SCENES_FOLDER: Path = ROBOTOOLS_ROOT.joinpath('scenes')


def icon_path(file_name: str) -> Path:
    """
    Get the path to an icon stored in the icon directory
    @param file_name:
    @return:
    """
    return ICON_DIR.joinpath(file_name)
