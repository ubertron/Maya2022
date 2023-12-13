import pymel.core as pm
import maya.mel as mel
import logging

from typing import Sequence


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

DEFAULT_LAYER: str = 'defaultLayer'
DISPLAY_LAYER: str = 'displayLayer'
REFERENCE_LAYER: str = 'referenceLayer'


def list_display_layers():
    layers = pm.ls(type=DISPLAY_LAYER)
    return layers


def create_display_layer(name: str) -> object:
    """
    Create a new display layer with a name
    @param name:
    @return:
    """
    display_layer = next((item for item in list_display_layers() if item == name), None)
    return display_layer if display_layer else pm.createDisplayLayer(name=name, empty=True)


def delete_display_layer(name):
    if name in list_display_layers():
        pm.delete(name)


def add_to_layer(objects: Sequence[pm.nodetypes.Transform], layer: str):
    if layer not in list_display_layers():
        create_display_layer(layer)

    pm.editDisplayLayerMembers(layer, objects)


def remove_from_layer(objects: Sequence[pm.nodetypes.Transform]):
    pm.editDisplayLayerMembers(DEFAULT_LAYER, objects)


def toggle_layer_shading(layer: str):
    if isinstance(layer, str):
        layer = pm.ls(layer)
        if layer:
            layer = layer[0]

    if layer in list_display_layers():
        pm.setAttr(layer.shading, (1 - pm.getAttr(layer.shading)))
    else:
        logging.info('Nope')


def list_layer_contents(layer_name: str):
    if layer_name in list_display_layers():
        return pm.editDisplayLayerMembers(layer_name, query=True)
    else:
        return None


def delete_empty_layers():
    for item in list_display_layers():
        if not list_layer_contents(item) and item != DEFAULT_LAYER:
            delete_display_layer(item)


def add_to_reference_layer(items: Sequence[pm.nodetypes.Transform] = ()):
    """
    Add selected objects to a reference layer
    @param items:
    """
    items = pm.ls(items, transforms=True) if items else pm.ls(sl=True, transforms=True)

    if len(items) > 0:
        if REFERENCE_LAYER not in list_display_layers():
            reference_layer = create_display_layer(REFERENCE_LAYER)
            pm.setAttr(reference_layer.shading, False)
            pm.setAttr(reference_layer.displayType, 2)

        add_to_layer(items, REFERENCE_LAYER)


def get_selected_display_layers():
    layers = mel.eval('getLayerSelection("Display")')
    return [item for item in list_display_layers() if item in layers]


def toggle_current_layer_shading():
    for layer in get_selected_display_layers():
        toggle_layer_shading(layer)


def set_display_layer_color(display_layer, color):
    pm.setAttr(display_layer.overrideColorRGB, [i / 255.0 for i in color])
    pm.setAttr(display_layer.overrideRGBColors, True)


def get_display_layers(nodes=None):
    return pm.listConnections(pm.ls(nodes, tr=True) if nodes else get_selected_transforms(), type=DISPLAY_LAYER)
