from pathlib import Path

from robotools.maya_environment import get_environment_variable

ROBOTOOLS_ROOT: Path = Path(get_environment_variable('ROBOTOOLS_ROOT')[0])
ICON_DIR: Path = ROBOTOOLS_ROOT.joinpath('icons')


def icon_path(file_name: str) -> Path:
    return ICON_DIR.joinpath(file_name)
