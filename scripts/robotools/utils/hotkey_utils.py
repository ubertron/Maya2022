import pymel.core as pm
import os

from pymel.core import Path


def set_hotkey(name, annotation, key, mel_command=None, python=None, alt=False, ctrl=False, cmd=False, overwrite=False):
    """
    Set a hotkey
    @param name:
    @param annotation:
    @param mel_command:
    @param python:
    @param key:
    @param alt:
    @param ctrl:
    @param cmd:
    @param overwrite:
    """
    if not overwrite:
        result = check_hotkey(key, alt, ctrl, cmd)
        if result is not None:
            pm.warning('Failed to set hotkey {} alt: {} ctrl: {} cmd: {}'.format(key, alt, ctrl, cmd))
            return

    command = mel_command if mel_command else python_command(python)
    pm.nameCommand(name, annotation=annotation, command=command)
    pm.hotkey(keyShortcut=key, altModifier=alt, ctrlModifier=ctrl, commandModifier=cmd, name=name)


def check_hotkey(key, alt=False, ctrl=False, cmd=False, clear=False):
    """
    Check if hotkey is being used
    Option to clear
    @param key:
    @param alt:
    @param ctrl:
    @param cmd:
    @param clear:
    """
    current_command = pm.hotkeyCheck(key=key, altModifier=alt, ctrlModifier=ctrl, commandModifier=cmd)
    if current_command:
        logging.info('Hotkey found: {}'.format(current_command))
    else:
        logging.info('Hotkey available')
        return None

    if current_command is not None and clear:
        pm.hotkey(k=key, altModifier=alt, ctrlModifier=ctrl, commandModifier=cmd, n='', rn='')

    if not clear:
        return current_command


def python_command(script):
    """
    Convert a python script to a string command
    @param script:
    @return:
    """
    return 'python("{}")'.format(script)


def hotkey_example():
    cmd = 'from maya_tools.mirror_utils import mirror_geometry; mirror_geometry(verbose=True)'
    set_hotkey('mirrorGeometryCommand', annotation='Mirror Geometry', python=cmd, key='F5', alt=True)
    logging.info('mirrorGeometryCommand set to F5 + alt')
    print_command = 'print(\'Hello world\')'
    set_hotkey('testCommand', annotation='Test Command', python=print_command, key='F6', alt=True)
    logging.info('testCommand set to F6 + alt')
    check_hotkey('F12', alt=True, ctrl=False)


class HotkeyManager(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path

        # Make a custom key set since Maya's default is locked.
        if not pm.hotkeySet(name, exists=True):
            pm.hotkeySet(name, source='Maya_Default')

        # set the current hotkey set
        pm.hotkeySet(name, edit=True, current=True)

    def delete_set(self):
        """
        Delete the hotkey set
        """
        pm.hotkeySet(self.name, edit=True, delete=True)

    def export_set(self):
        """
        Export the hotkeys to the stated path
        """
        pm.hotkeySet(self.name, edit=True, export=self.path)

    @property
    def exists(self):
        return Path(self.path).exists()

    def import_set(self):
        """
        Import the hotkeys from the stated path
        """
        assert self.exists, 'Hotkey set {} not found'.format(self.name)

        if pm.hotkeySet(self.name, exists=True):
            self.delete_set()

        pm.hotkeySet(edit=True, ip=self.path)

    @staticmethod
    def set_hotkey(name, annotation, key, mel_command=None, python=None, alt=False, ctrl=False, cmd=False,
                   overwrite=False):
        """
        Set a hotkey
        @param name:
        @param annotation:
        @param key:
        @param mel_command:
        @param python:
        @param alt:
        @param ctrl:
        @param cmd:
        @param overwrite:
        """
        set_hotkey(name, annotation, key, mel_command, python, alt, ctrl, cmd, overwrite)

    @staticmethod
    def check_hotkey(key, alt=False, ctrl=False, cmd=False, clear=False):
        """
        Check/clear a hotkey
        @param key:
        @param alt:
        @param ctrl:
        @param cmd:
        @param clear:
        """
        check_hotkey(key, alt, ctrl, cmd, clear)
