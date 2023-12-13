import math
import pymel.core as pm

from typing import Optional
from maya import mel

from robotools.node_utils import State, is_node_type, set_component_mode, get_component_indices, get_component_mode, \
    select_components, encode_components, reset_pivot
from robotools.robotools_enums import Axis, ComponentType


def merge_vertices(transform: Optional[pm.nt.Transform] = None, precision: int = 5) -> pm.nt.PolyMergeVert:
    """
    Merge vertices on a selected or supplied object
    @param transform:
    @param precision:
    @return:
    """
    transform = pm.ls(transform, tr=True) if transform else pm.ls(sl=True, tr=True)
    result = pm.polyMergeVertex(transform, distance=precision_to_threshold(precision))
    return pm.ls(result[0])[0]


def precision_to_threshold(precision: int = 1) -> float:
    """
    Converts precision accuracy to a float
    @param precision:
    @return:
    """
    return 1.0 / math.pow(10, precision)


def get_selected_geometry():
    state = State()
    set_component_mode(ComponentType.object)
    geometry_list = [item for item in pm.ls(sl=True, transforms=True)
                     if is_node_type(item, 'mesh')]
    state.restore()
    return geometry_list


def get_selected_vertices(obj):
    state = State()
    pm.select(obj)
    set_component_mode(ComponentType.vertex)
    components = pm.ls(sl=True)
    selection = [] if components == [] else get_component_indices(components)
    state.restore()
    return selection


def get_selected_edges(obj):
    state = State()
    pm.select(obj)
    pm.selectMode(component=True)
    pm.selectType(edge=True)
    set_component_mode(ComponentType.edge)
    components = pm.ls(sl=True)
    selection = [] if components == [] else get_component_indices(components)
    pm.select(clear=True)
    state.restore()
    return selection


def get_selected_faces(obj):
    state = State()
    pm.select(obj)
    set_component_mode(ComponentType.face)
    components = pm.ls(sl=True)
    selection = [] if components == [] else get_component_indices(components)
    state.restore()
    return selection


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


def slice_geometry(nodes=None, axis=Axis.x, positive=True):
    """
    Slice polygon geometry along an axis
    @param nodes:
    @param axis:
    @param positive:
    """
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


def mirror_geometry(nodes=None, axis=Axis.x, positive=False, merge_threshold=0.001):
    """
    Mirror polygon geometry along an axis
    @param nodes:
    @param axis:
    @param positive:
    @param merge_threshold:
    """
    state = State()
    set_component_mode(ComponentType.object)
    nodes = pm.ls(nodes) if nodes else pm.ls(sl=True, tr=True)
    direction = {Axis.x: 0 + positive, Axis.y: 2 + positive, Axis.z: 4 + positive}

    for item in nodes:
        pivot_position = [pm.xform(item, query=True, piv=True, ws=True)[i] for i in range(3)]
        slice_geometry(item, axis, not positive)
        pm.polyMirrorFace(item, ws=True, d=direction[axis], mergeMode=1, p=pivot_position, mt=merge_threshold, mtt=1)

    state.restore()


def connect_edges(edge_flow=False):
    if get_component_mode() == ComponentType.edge and len(pm.ls(sl=True)):
        pm.polyConnectComponents(pm.ls(sl=True), insertWithEdgeFlow=1 if edge_flow else 0, adjustEdgeFlow=1)


def relax_vertices(nodes=None, iterations=2, history=False):
    state = State()
    for n in pm.ls(nodes, tr=True) if nodes else get_selected_geometry():
        selected_vertices = get_selected_vertices(n)
        indices = selected_vertices if selected_vertices else range(len(n.vtx))
        pm.polyAverageVertex(n.vtx[indices], iterations=iterations, ch=history)
    state.restore()


def extract_selected_faces():
    if get_component_mode() == ComponentType.face:
        state = State()
        dupe_list = []
        for item in state.object_selection:
            pm.hilite(item, replace=True)
            faces = get_component_indices()
            if faces:
                dupe_list.append(extract_faces(item, faces, False))
        if dupe_list:
            set_component_mode(ComponentType.object)
            pm.select(dupe_list)
            return dupe_list
        else:
            pm.warning('No faces selected')
            state.restore()
    else:
        pm.warning('Select faces in face component mode.')


def extract_faces(node, faces, restore_state=True):
    state = State()
    inverse_faces = [i for i in range(node.faces.count()) if i not in faces]
    dupe = pm.duplicate(node)[0]
    pm.rename(dupe, '{}_extraction'.format(node.name()))
    pm.delete(encode_components(node, faces, ComponentType.face))
    pm.delete(encode_components(dupe, inverse_faces, ComponentType.face))
    if restore_state:
        state.restore()
        if node in state.object_selection:
            pm.select(dupe, add=True)
    return dupe


def combine(nodes=None, construction_history=False):
    state = State()
    nodes = pm.ls(nodes) if nodes else pm.ls(sl=True, transforms=True)
    nodes = [item for item in nodes if is_node_type(item, pm.nodetypes.mesh)]
    select_combined = list(
        set(nodes).intersection(state.object_selection)) and state.component_mode == ComponentType.object
    if len(nodes) > 1:
        state.remove_objects(nodes)  # Has to be done manually before objects are combined
        new_name = nodes[-1].name()
        pivot_position = pm.getAttr(nodes[-1].translate)
        new_object = pm.polyUnite(nodes, ch=construction_history)[0]
        pm.rename(new_object, new_name)
        pm.xform(new_object, worldSpace=True, rotatePivot=pivot_position)
        pm.xform(new_object, worldSpace=True, scalePivot=pivot_position)
        reset_pivot(new_object)
        state.restore()
        if select_combined:
            pm.select(new_object, add=True)
        return new_object
    else:
        pm.warning('Please select more than one valid object.')


def quadrangulate():
    """
    Quadrangulate selection
    """
    pm.runtime.Quadrangulate()


def target_weld():
    """
    Start target weld mode
    """
    mel.eval('dR_targetWeldTool')
