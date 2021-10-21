import pymel.core as pm
import random

from ad_tools import ad_node, ad_poly

def random_vector3():
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
            color_value = str(pm.polyColorPerVertex(node.f[fid], q=True, colorRGB=True))
            if color_value in color_dict.keys():
                color_dict[color_value].append(fid)
            else:
                color_dict[color_value] = [fid]
    return color_dict

def select_faces_by_selected_vertex_colors(transforms=None):
    for node in ad_node.get_transforms(transforms):
        selected_colors = []
        for fid in ad_node.get_selected_faces(node):
            selected_colors.append(
                str(pm.polyColorPerVertex(node.f[fid], q=True, colorRGB=True)))
        color_dict = get_face_vertex_color_dict(node)
        for color_value in list(set(selected_colors)):
            pm.select(node.f[color_dict[color_value]], add=True)

def select_faces_by_vertex_color(color, transforms=None):
    rgb = str([x/255 for x in color])
    print(rgb)
    for node in ad_node.get_transforms(transforms):
        print(get_face_vertex_color_dict(node).keys())
        faces = get_face_vertex_color_dict(node).get(rgb)
        if faces:
            pm.select(node.f[faces])

