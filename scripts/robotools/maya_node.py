import pymel.core as pm
import random

from typing import Sequence


def get_world_space_translation(transform):
    return pm.xform(transform, query=True, worldSpace=True, rotatePivot=True)


def create_locator(translation: Sequence[float, float, float], local_scale: float = 0.1):
    """
    Create a space locator
    @param translation:
    @param local_scale:
    @return:
    """
    locator = pm.spaceLocator()
    pm.setAttr(locator.translate, translation, type='float3')
    pm.setAttr(locator.localScaleX, local_scale)
    pm.setAttr(locator.localScaleY, local_scale)
    pm.setAttr(locator.localScaleZ, local_scale)

    return locator


def create_random_locators(count: int, scale: float = 2.0, planar: bool = True):
    """
    Create a random set of locators
    @param count:
    @param scale:
    @param planar:
    @return:
    """
    locators = []
    for i in range(count):
        tx = 0 if planar else random.uniform(0, scale)
        ty = random.uniform(0, scale)
        tz = random.uniform(0, scale)
        locators.append(create_locator((tx, ty, tz)))
    return locators


def set_random_hierarchy(transforms):
    for i, v in enumerate(transforms[1:]):
        pm.parent(v, random.choice(transforms[:i + 1]))


def create_random_symmetrical_hierarchy(count, scale):
    root_locator = create_locator(
        (0, random.uniform(0, scale), random.uniform(0, scale)))
    spine = [root_locator]
    limbs = []
    for i in range(count):
        if random.choice([True, False]):
            locator = create_locator(
                (0, random.uniform(0, scale), random.uniform(0, scale)))
            pm.parent(locator, random.choice(spine))
            spine.append(locator)
        else:
            position = [random.uniform(0, scale), random.uniform(0, scale),
                        random.uniform(0, scale)]
            limb_l = create_locator((-position[0], position[1], position[2]))
            limb_r = create_locator((position[0], position[1], position[2]))
            if limbs and random.choice([True, False]):
                limb_parent = random.choice(limbs)
                pm.parent(limb_l, limb_parent[0])
                pm.parent(limb_r, limb_parent[1])
            else:
                spine_parent = random.choice(spine)
                pm.parent(limb_l, spine_parent)
                pm.parent(limb_r, spine_parent)
            limbs.append((limb_l, limb_r))
    return root_locator


# --------------------------------------------------------------------------------------
# STATE
# --------------------------------------------------------------------------------------


class State:
    """Query and restore selection/component mode"""

    def __init__(self):
        self.component_mode = get_component_mode()
        self.selection = pm.ls(sl=True)
        if self.object_mode:
            self.object_selection = pm.ls(sl=True)
            self.component_selection = []
        else:
            self.component_selection = pm.ls(sl=True)
            set_component_mode(ComponentType.object)
            self.object_selection = pm.ls(sl=True)
            set_component_mode(self.component_mode)
            pm.hilite(self.object_selection)

    def restore(self):
        if self.object_selection:
            pm.select(self.object_selection, noExpand=True)
            set_component_mode(self.component_mode)
        else:
            set_component_mode(ComponentType.object)
            pm.select(clear=True)
        if not self.object_mode:
            pm.select(self.component_selection)

    @property
    def object_mode(self):
        return self.component_mode == ComponentType.object

    def remove_objects(self, objects):
        # Sometimes necessary as pm.objExists check causes an exception
        for item in list(objects):
            if item in self.object_selection:
                self.object_selection.remove(item)


# --------------------------------------------------------------------------------------
# COMPONENTS
# --------------------------------------------------------------------------------------


class ComponentType:
    vertex = 'vertex'
    edge = 'edge'
    face = 'face'
    object = 'object'
    vertex_face = 'vertex face'
    element = 'element'
    uv = 'uv'


def get_component_mode():
    if pm.selectMode(query=True, object=True):
        return ComponentType.object
    elif pm.selectType(query=True, vertex=True):
        return ComponentType.vertex
    elif pm.selectType(query=True, edge=True):
        return ComponentType.edge
    elif pm.selectType(query=True, facet=True):
        return ComponentType.face
    elif pm.selectType(query=True, polymeshUV=True):
        return ComponentType.uv
    else:
        return 'unknown'


def set_component_mode(component_type=ComponentType.object):
    if component_type == ComponentType.object:
        pm.selectMode(object=True)
    else:
        pm.selectMode(component=True)
        if component_type == ComponentType.vertex:
            pm.selectType(vertex=True)
        elif component_type == ComponentType.edge:
            pm.selectType(edge=True)
        elif component_type == ComponentType.face:
            pm.selectType(facet=True)
        elif component_type == ComponentType.uv:
            pm.selectType(polymeshUV=True)
        else:
            pm.warning('Unknown component type')


def get_component_indices(components=None):
    """Gets the components selected in the current component mode"""
    return [i.index() for i in (
        pm.ls(components, flatten=True) if components else pm.ls(sl=True,
                                                                 flatten=True))]


def encode_components(obj, component_list, component_type=ComponentType.face):
    """Convert a list of component indices into a component selection"""
    flag_dict = {
        ComponentType.vertex: 'vtx',
        ComponentType.edge: 'edge',
        ComponentType.face: 'f',
        ComponentType.uv: 'map'
    }
    return [f'{obj}.{flag_dict.get(component_type)}[{i}]' for i in component_list]


def select_components(obj, components, component_type=ComponentType.face, hilite=True):
    state = State()
    if component_type == ComponentType.vertex:
        pm.select(obj.vtx[components])
    elif component_type == ComponentType.edge:
        pm.select(obj.e[components])
    elif component_type == ComponentType.face:
        pm.select(obj.f[components])
    elif component_type == ComponentType.uv:
        pm.select(obj.map[components])
    else:
        pm.warning('Component type not supported')
    if hilite:
        pm.hilite(obj)
    else:
        state.restore()


def get_selected_components(obj, component_type):
    state = State()
    pm.select(obj)
    set_component_mode(component_type)
    components = pm.ls(sl=True)
    selection = [] if components == [] else get_component_indices(components)
    state.restore()
    return selection


def get_selected_vertices(obj):
    return get_selected_components(obj, ComponentType.vertex)


def get_selected_edges(obj):
    # n.b. different code path for edges in Maya 2018
    return get_selected_components(obj, ComponentType.edge)


def get_selected_faces(obj):
    return get_selected_components(obj, ComponentType.face)


# --------------------------------------------------------------------------------------
# NODES, SHAPES AND TRANSFORMS
# --------------------------------------------------------------------------------------

def get_selected_transforms():
    state = State()
    set_component_mode(ComponentType.object)
    selection = pm.ls(sl=True, tr=True)
    state.restore()
    return selection


def get_transforms(nodes=None):
    state = State()
    set_component_mode(ComponentType.object)
    selection = pm.ls(nodes, tr=True) if nodes else pm.ls(sl=True, tr=True)
    state.restore()
    return selection


def get_shapes_from_transform(xform_node, full_path=False):
    return pm.listRelatives(xform_node, f=full_path, shapes=True) if pm.nodeType(
        xform_node) == 'transform' else None


def get_transform_from_shape(node, full_path=False):
    return node if pm.nodeType(node) == 'transform' else \
        pm.listRelatives(node, fullPath=full_path, parent=True)[0]


def is_node_type(obj, node_type):
    shape = get_shapes_from_transform(obj)
    return node_type == pm.nodeType(shape[0]) if shape else None


def super_reset(nodes=None):
    nodes = pm.ls(nodes, tr=True) if nodes else pm.ls(sl=True, tr=True)
    freeze_transformations(nodes)
    reset_pivot(nodes)
    delete_history(nodes)


def freeze_transformations(pm_obj=None):
    for node in list(pm_obj) if pm_obj else pm.ls(sl=True, tr=True):
        pm.makeIdentity(node, apply=True, translate=True, rotate=True, scale=True)


def reset_pivot(nodes=None):
    for item in pm.ls(nodes, tr=True) if nodes else pm.ls(sl=True, tr=True):
        pivot_node = pm.xform(item, query=True, worldSpace=True, rotatePivot=True)
        pm.xform(item, relative=True, translation=[-i for i in pivot_node])
        pm.makeIdentity(item, apply=True, translate=True)
        pm.xform(item, translation=pivot_node)


def delete_history(nodes=None):
    state = State()
    set_component_mode(ComponentType.object)
    pm.delete(pm.ls(nodes, tr=True) if nodes else pm.ls(sl=True, tr=True), constructionHistory=True)
    state.restore()
