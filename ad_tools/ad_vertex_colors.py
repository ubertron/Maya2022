import pymel.core as pm
import random

from typing import Any
from ad_tools import ad_node, ad_poly


def random_vector3() -> list:
    return [random.uniform(0, 1) for _ in range(3)]


def apply_vertex_color(rgb_color=None, display=True):
    vertex_color = rgb_color if rgb_color else random_vector3()
    if ad_node.get_component_mode() == ad_node.ComponentType.face:
        for obj in ad_poly.get_selected_geometry():
            for face in ad_node.get_selected_faces(obj):
                pm.polyColorPerVertex(obj.f[face], colorRGB=vertex_color, cdo=display)


def remove_vertex_color(display=True):
    if ad_node.get_component_mode() == ad_node.ComponentType.face:
        for obj in ad_poly.get_selected_geometry():
            for face in ad_node.get_selected_faces(obj):
                pm.polyColorPerVertex(obj.f[face], remove=True, cdo=display)


def get_face_vertex_color_dict(node):
    color_dict = {}
    if pm.polyColorSet(node, q=True, currentColorSet=True):
        for fid in range(node.faces.count()):
            color_value = pm.polyColorPerVertex(node.f[fid], q=True, colorRGB=True)
            color_key = formatted_color(color_value)
            if color_key in color_dict.keys():
                color_dict[color_key].append(fid)
            else:
                color_dict[color_key] = [fid]
    return color_dict


def select_faces_by_selected_vertex_colors(transforms=None):
    for node in ad_node.get_transforms(transforms):
        selected_colors = []
        for fid in ad_node.get_selected_faces(node):
            color_value = pm.polyColorPerVertex(node.f[fid], q=True, colorRGB=True)
            selected_colors.append(formatted_color(color_value))
        color_dict = get_face_vertex_color_dict(node)
        for color_value in list(set(selected_colors)):
            pm.select(node.f[color_dict[color_value]], add=True)


def select_faces_by_vertex_color(color: Any, transforms=None):
    transforms = ad_node.get_transforms(transforms)
    # pm.select(clear=True)
    for node in transforms:
        faces = get_face_vertex_color_dict(node).get(str(color))
        if faces:
            pm.select(node.f[faces], add=True)
            # pm.hilite(node)
    # pm.select(transforms)
    pm.hilite(transforms)


def formatted_color(rgb_float_list: Any, precision: int = 4) -> str:
    return str([round(x, precision) for x in rgb_float_list])
