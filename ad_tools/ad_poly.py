import pymel.core as pm

from ad_tools.ad_node import State, ComponentType, is_node_type, set_component_mode, \
    get_component_indices


def get_selected_geometry():
    state = State()
    set_component_mode(ComponentType.object)
    geometry_list = [item for item in pm.ls(sl=True, transforms=True)
                     if is_node_type(item, 'mesh')]
    state.restore()
    return geometry_list

def get_faces_from_edge(obj, edge):
    return get_component_indices(
        pm.polyListComponentConversion(obj.e[edge], toFace=True))

def get_edges_from_face(obj, face):
    return get_component_indices(
        pm.polyListComponentConversion(obj.f[face], toEdge=True))

def get_vertices_from_edge(obj, edge):
    return get_component_indices(
        pm.polyListComponentConversion(obj.e[edge], toVertex=True))

def get_edges_from_vertex(obj, vertex):
    return get_component_indices(
        pm.polyListComponentConversion(obj.vtx[vertex], toEdge=True))

def get_vertices_from_faces(obj, faces):
    return get_component_indices(
        pm.polyListComponentConversion(obj.f[faces], toVertex=True))

def convert_components(obj, components=None, from_type=ComponentType.face,
                       to_type=ComponentType.edge, select=False):
    state = State()
    set_component_mode(from_type)
    if components:
        select_components(obj, components, from_type)
    result = pm.polyListComponentConversion(pm.ls(sl=True),
                                            fv=from_type == ComponentType.vertex,
                                            fe=from_type == ComponentType.edge,
                                            ff=from_type == ComponentType.face,
                                            fuv=from_type == ComponentType.uv,
                                            tv=to_type == ComponentType.vertex,
                                            te=to_type == ComponentType.edge,
                                            tf=to_type == ComponentType.face,
                                            tuv=to_type == ComponentType.uv)
    if select:
        pm.select(result)
    else:
        state.restore()
    return [i.index() for i in pm.ls(result, flatten=True)]
