import pymel.core as pm

from ad_tools.ad_node import State, ComponentType, is_node_type, set_component_mode, \
    get_component_indices
from ad_tools import Axis


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


def cleft_in_twain(nodes=None, axis=Axis.x, positive=True):
    state = State()
    set_component_mode(ComponentType.object)
    nodes = pm.ls(nodes) if nodes else pm.ls(sl=True, tr=True)
    angles = {
        Axis.x: [0, positive * 180 - 90, 0],
        Axis.y: [90 - positive * 180, 0, 0],
        Axis.z: [0, 180 - positive * 180, 0]
    }
    cut_axis = angles[axis]

    for item in nodes:
        pm.select(item)
        pivot_matrix = pm.xform(query=True, piv=True, ws=True)
        pivot_position = [pivot_matrix[0], pivot_matrix[1], pivot_matrix[2]]
        pm.polyCut(
            cutPlaneCenter=pivot_position,
            cutPlaneRotate=cut_axis,
            extractFaces=True,
            extractOffset=[0, 0, 0],
            deleteFaces=True
        )

    state.restore()


def mirror(nodes=None, axis=Axis.x, positive=False, merge_threshold=0.001):
    state = State()
    set_component_mode(ComponentType.object)
    nodes = pm.ls(nodes) if nodes else pm.ls(sl=True, tr=True)
    direction = {
        Axis.x: 0 + positive,
        Axis.y: 2 + positive,
        Axis.z: 4 + positive
    }

    for item in nodes:
        pivot_position = [pm.xform(item, query=True, piv=True, ws=True)[i] for i in range(3)]
        cleft_in_twain(item, axis, not positive)
        pm.polyMirrorFace(item, ws=True, d=direction[axis], mergeMode=1, p=pivot_position, mt=merge_threshold)

    state.restore()
