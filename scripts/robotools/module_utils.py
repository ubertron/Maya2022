import pymel.util

from pathlib import Path
from typing import List


LOCAL_MAYA_MODULE_DIRECTORY: Path = Path(pymel.util.getEnv('MAYA_APP_DIR')).joinpath('modules')
LOCAL_MAYA_MODULE_FILES: List[Path] = LOCAL_MAYA_MODULE_DIRECTORY.glob('*.mod')


def get_module_files(root: Path):
    """
    Get a list of all module files within a root directory
    """
    return root.rglob('*.mod')


def format_module_files():
    """
    Print out module locations
    """
    from common_lib import PYTHON_TOOLS
    
    local_files = [str(x) for x in LOCAL_MAYA_MODULE_FILES]
    project_files = [str(x) for x in get_module_files(PYTHON_TOOLS)]
    print(f'Local modules [{LOCAL_MAYA_MODULE_DIRECTORY}]: \n' + '\n'.join(local_files))
    print(f'\nProject modules found [{PYTHON_TOOLS}]: \n' + '\n'.join(project_files))


if __name__ == '__main__':
    format_module_files()
