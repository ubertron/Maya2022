import logging

from maya.OpenMayaUI import MQtUtil
import pymel.core as pm
from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance
from typing import Type, List
from importlib import reload

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

MAYA_MAIN_WINDOW: QWidget = wrapInstance(int(MQtUtil.mainWindow()), QWidget)


def getWidget(widget_class: Type[QWidget], first_only: bool = True) -> Type[QWidget] or List[Type[QWidget]] or None:
    """
    Finds instances of the passed widget classes in Maya
    @param widget_class: the widget class
    @param first_only: set to true to only pass the first instance
    @return:
    """
    for x in MAYA_MAIN_WINDOW.children():
        print(x)
    if first_only:
        return next((x for x in MAYA_MAIN_WINDOW.children() if type(x) is widget_class), None)
    else:
        return [x for x in MAYA_MAIN_WINDOW.children() if type(x) is widget_class]


def launchUtility(module: Type, utility_class: Type, **kwargs):
    """
    Handles the reloading of utilities avoiding duplication
    Reload is necessary because Maya's garbage collection can nuke classes
    :param module:
    :param utility_class:
    :param kwargs:
    """
    utility = getWidget(widget_class=utility_class)
    if utility:
        utility.deleteLater()
        reload(module)
    utility = utility_class(**kwargs)
    utility.show()
