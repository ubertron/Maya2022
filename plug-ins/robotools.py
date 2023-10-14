# https://help.autodesk.com/view/MAYAUL/2023/ENU/?guid=Maya_SDK_A_First_Plugin_Python_HelloWorldAPI2_html
import os
import sys
import maya.api.OpenMaya as om
import logging
import pymel.util
import platform

from maya import mel
from pathlib import Path


USER_FOLDER = Path.home().parent if Path.home().name == 'Documents' else Path.home()
ROBOTOOLS_ROOT: Path = USER_FOLDER.joinpath('Documents', 'Projects', 'Maya2022')
ROBOTOOLS_SCRIPTS: Path = ROBOTOOLS_ROOT.joinpath('scripts')
SITE_PACKAGES: Path = ROBOTOOLS_ROOT.joinpath('site-packages')
ROBOTOOLS_PLUG_INS: Path = ROBOTOOLS_ROOT.joinpath('plug-ins')
ENVIRONMENT_PATHS = {
    'PYTHONPATH': [ROBOTOOLS_SCRIPTS.as_posix(), SITE_PACKAGES.as_posix()],
    'MAYA_PLUG_IN_PATH': [ROBOTOOLS_PLUG_INS.as_posix()],
    'ROBOTOOLS_ROOT': [ROBOTOOLS_ROOT.as_posix()]
}
PLATFORM_SEPARATOR = ':' if platform.system() == 'Darwin' else ';'


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
class RobotoolsInitializeCmd(om.MPxCommand):
    kPluginCmdName = 'RobotoolsInitialize'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return RobotoolsInitializeCmd()

    def doIt(self, args):
        raise Exception('Plugin not supposed to be invoked - only loaded or unloaded.')


def initializePlugin(plugin):
    """
    Initialize the plug-in
    @param plugin:
    """
    vendor = 'Robonobo'
    version = '1.0.0'
    pluginFn = om.MFnPlugin(plugin, vendor, version)
    try:
        bootstrap()
        pluginFn.registerCommand(RobotoolsInitializeCmd.kPluginCmdName, RobotoolsInitializeCmd.cmdCreator)
    except RuntimeError:
        raise RuntimeError('Failed to register command: %s\n' % RobotoolsInitializeCmd.kPluginCmdName)


def uninitializePlugin(plugin):
    """
    Uninitialize the plugin
    @param plugin:
    """
    pluginFn = om.MFnPlugin(plugin)
    try:
        teardown()
        pluginFn.deregisterCommand(RobotoolsInitializeCmd.kPluginCmdName)
    except RuntimeError:
        raise RuntimeError('Failed to unregister command: %s\n' % RobotoolsInitializeCmd.kPluginCmdName)


def bootstrap():
    """
    Set up Robotools
    """
    logging.info('-------- Robotools Bootstrapping --------')

    for path in ENVIRONMENT_PATHS['PYTHONPATH']:
        if path not in sys.path:
            sys.path.append(path)
            logging.info('Tools path added: %s' % path)

    for env_key in ENVIRONMENT_PATHS.keys():
        environment_values = get_environment_variable(env_key)
        environment_values.extend(ENVIRONMENT_PATHS[env_key])
        environment_values = list(set(environment_values))
        environment_values.sort(key=lambda x: x.lower())
        set_environment_variable(env_key, environment_values)

    logging.info(get_environment_variable('ROBOTOOLS_ROOT'))

    from robotools import shelf_manager
    shelf_manager.setup_robotools_shelf()


def teardown():
    """
    Reverse the bootstrapping to unload the plug-in
    """
    for path in ENVIRONMENT_PATHS['PYTHONPATH']:
        if path in sys.path:
            sys.path.remove(path)

    for env_key in ENVIRONMENT_PATHS.keys():
        environment_values = get_environment_variable(env_key)
        reduced = [path for path in environment_values if path not in ENVIRONMENT_PATHS[env_key]]
        set_environment_variable(env_key, reduced)


def get_environment_variable(variable_name):
    """
    Get a list of the values for an environment variable
    @param variable_name:
    @return:
    """
    result = mel.eval('getenv "%s"' % variable_name).split(PLATFORM_SEPARATOR)
    return [x for x in result if x != '']


def set_environment_variable(variable_name, value_list):
    """
    Set an environment variable with a list of values
    @param variable_name:
    @param value_list:
    """
    mel.eval('putenv "%s" "%s"' % (variable_name, PLATFORM_SEPARATOR.join(value_list)))