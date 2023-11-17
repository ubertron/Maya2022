import pymel.core as pm


def initialize_hotkeys():
    hotkey_test_command = "hotkeyTest"
    pm.hotkey(keyShortcut='x', ctrlModifier=True, altModifier=True, name='')
    pm.nameCommand(hotkey_test_command, annotation='Hotkey Test', command='python("print(\"hot key test\")")')
    pm.hotkey(keyShortcut='x', ctrlModifier=True, altModifier=True, name=hotkey_test_command)


initialize_hotkeys()
