import pymel.core as pm
import maya.mel as mel


def list_display_layers():
    layers = pm.ls(type='displayLayer')
    return layers


def create_display_layer(name):
    display_layer = next((item for item in list_display_layers() if item == name), None)
    if not display_layer:
        display_layer = pm.createDisplayLayer(name=name, empty=True)
    return display_layer


def delete_display_layer(name):
    if name in list_display_layers():
        pm.delete(name)


def add_to_layer(objects, layer):
    if layer not in list_display_layers():
        create_display_layer(layer)
    pm.editDisplayLayerMembers(layer, objects)


def remove_from_layer(objects):
    pm.editDisplayLayerMembers('defaultLayer', objects)


def toggle_layer_shading(layer):
    if isinstance(layer, str):
        layer = pm.ls(layer)
        if layer:
            layer = layer[0]
    if layer in list_display_layers():
        pm.setAttr(layer.shading, (1 - pm.getAttr(layer.shading)))
    else:
        print('Nope')


def list_layer_contents(layer_name):
    if layer_name in list_display_layers():
        return pm.editDisplayLayerMembers(layer_name, query=True)
    else:
        return None


def delete_empty_layers():
    for item in list_display_layers():
        if not list_layer_contents(item) and item != 'defaultLayer':
            delete_display_layer(item)


def add_to_reference_layer(items=()):
    items = items if items else pm.ls(sl=True, transforms=True)
    if len(items) > 0:
        if 'referenceLayer' not in list_display_layers():
            reference_layer = create_display_layer('referenceLayer')
            pm.setAttr(reference_layer.shading, False)
            pm.setAttr(reference_layer.displayType, 2)
        add_to_layer(items, 'referenceLayer')


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
    return pm.listConnections(pm.ls(nodes, tr=True) if nodes else get_selected_transforms(), type='displayLayer')
