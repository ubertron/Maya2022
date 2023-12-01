import os
import sys
import maya.api.OpenMaya as om
import logging
import pymel.util
import platform

from maya import mel
from pathlib import Path

from robotools import robotools_utils


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class RobotoolsShelfInitializeCmd(om.MPxCommand):
    kPluginCmdName = 'RobotoolsShelfInitialize'

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return RobotoolsShelfInitializeCmd()

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
        robotools_utils.setup_robotools_shelf()
        logging.info('>>>> Initializing Robotools Shelf')
        hotkey_manager = robotools_utils.RobotoolsHotkeyManager()

        if hotkey_manager.exists:
            logging.info('>>>> Hotkeys imported')
            hotkey_manager.import_set()
        else:
            logging.info('>>>> Hotkey preferences file created')
            hotkey_manager.init_hotkeys()
            hotkey_manager.export_set()

        pluginFn.registerCommand(RobotoolsShelfInitializeCmd.kPluginCmdName, RobotoolsShelfInitializeCmd.cmdCreator)
    except RuntimeError:
        raise RuntimeError('Failed to register command: %s\n' % RobotoolsShelfInitializeCmd.kPluginCmdName)


def uninitializePlugin(plugin):
    """
    Uninitialize the plugin
    @param plugin:
    """
    pluginFn = om.MFnPlugin(plugin)

    try:
        from robotools import robotools_utils

        logging.info('>>>> Deleting Robotools Shelf')
        robotools_utils.delete_robotools_shelf()
        logging.info('>>>> Deleting Robotools Hotkeys')
        robotools_utils.RobotoolsHotkeyManager().delete_set()

        pluginFn.deregisterCommand(RobotoolsShelfInitializeCmd.kPluginCmdName)
    except RuntimeError:
        raise RuntimeError('Failed to unregister command: %s\n' % RobotoolsShelfInitializeCmd.kPluginCmdName)
