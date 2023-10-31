import pymel.util
import pymel.core as pm
import platform
import sys
import os

from pathlib import Path
from typing import List
from maya import mel
from dataclasses import dataclass

from robotools.environment_utils import get_environment_variable_paths

PLUG_IN_PATH_STR: str = 'MAYA_PLUG_IN_PATH'


def get_plug_in_paths(verbose: bool = False) -> List[Path]:
    """
    Check the paths listed in the MAYA_PLUG_IN_PATH environment variable
    @param verbose:
    @return:
    """
    return get_environment_variable_paths(variable_name=PLUG_IN_PATH_STR, verbose=verbose)


PLUG_IN_PATHS: List[Path] = get_plug_in_paths()


def get_loaded_plug_ins(verbose: bool = False):
    """
    Check the currently loaded plug-ins
    @param verbose:
    @return:
    """
    result = pm.pluginInfo(query=True, listPlugins=True)
    result.sort(key=lambda x: x.lower())

    if verbose:
        print('Loaded plug-ins:\n' + '\n'.join(result))

    return result


if __name__ == '__main__':
    get_plug_in_paths(verbose=True)
    get_loaded_plug_ins(verbose=True)
