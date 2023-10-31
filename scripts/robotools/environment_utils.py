import platform

from maya import mel
from typing import List
from pathlib import Path


PLATFORM_SEPARATOR = ':' if platform.system() == 'Darwin' else ';'


def get_environment_variable(variable_name) -> str:
    """
    Get a value for an environment variable
    @param variable_name:
    @return:
    """
    result = mel.eval(f'getenv {variable_name}')
    return [x for x in result if x != '']


def get_environment_variable_paths(variable_name: str, verbose: bool = False) -> List[Path]:
    """
    Get a list of paths for a variable that returns a path list
    @param variable_name:
    @param verbose:
    @return:
    """
    paths = mel.eval(f'getenv {variable_name}').split(PLATFORM_SEPARATOR)
    paths.sort(key=lambda x: x.lower())
    paths = [Path(x).resolve() for x in paths]

    if verbose:
        print(f"Paths for {variable_name}:\n" + "\n".join([str(x) for x in paths]))

    return paths


def set_environment_variable(variable_name, value_list):
    """
    Set an environment variable with a list of values
    @param variable_name:
    @param value_list:
    """
    mel.eval('putenv "%s" "%s"' % (variable_name, PLATFORM_SEPARATOR.join(value_list)))
