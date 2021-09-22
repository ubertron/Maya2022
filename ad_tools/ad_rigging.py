import pymel.core as pm
import numpy

from ad_tools import ad_node
from ad_tools.ad_layers import create_display_layer


class ConstraintType:
    point = 'point'
    orient = 'orient'
    parent = 'parent'


def create_rigging_layers():
    for i in ['geometry', 'skeleton', 'control', 'utility']:
        create_display_layer(f'{i}Layer')


def create_joints_from_transforms(transforms, scale=0.2):
    joints = []
    pm.select(clear=True)
    for i in transforms:
        joint = pm.joint(p=pm.getAttr(i.translate), radius=scale)
        joints.append(joint)
    reorient_joints(joints[0])
    return joints[0]


def create_joints_from_hierarchy(node, parent=None, scale=0.2):
    if parent:
        pm.select(parent)
    else:
        pm.select(clear=True)
    joint = pm.joint(p=ad_node.get_world_space_translation(node), radius=scale)
    for i in pm.listRelatives(node, children=True, type=pm.nodetypes.Transform):
        create_joints_from_hierarchy(i, parent=joint, scale=scale)
    return get_root_joint(joint)


def get_end_joints(node, joints=None):
    if joints is None:
        joints = []
    for i in pm.listRelatives(node):
        if pm.listRelatives(i):
            get_end_joints(i, joints)
        else:
            joints.append(i)
    return joints


def get_root_joint(joint):
    node = joint
    while pm.listRelatives(node, parent=True):
        node = pm.listRelatives(node, parent=True)[0]
    return node[0] if type(node) == list else node


def reorient_joints(root_joint):
    pm.joint(root_joint, edit=True, orientJoint='xyz', secondaryAxisOrient='xup', children=True, zeroScaleOrient=True)
    for i in get_end_joints(root_joint):
        pm.joint(i, edit=True, orientJoint='none')


def reorient_selected_joints():
    root_joint = ad_rigging.get_root_joint(pm.ls(sl=True, type=pm.nodetypes.Joint))
    if root_joint:
        ad_rigging.reorient_joints(root_joint)


def create_locators_from_joints(joint, parent=None):
    locator = ad_node.create_locator(ad_node.get_world_space_translation(joint))
    pm.parent(locator, parent)
    for i in pm.listRelatives(joint):
        create_locators_from_joints(i, locator)
    return get_root_joint(locator)


def create_control(joint, radius):
    """
    Creates an aligned NURBS circle control for a joint
    :param joint: the joint for the control
    :param radius: size of the control
    :return: the control
    """
    joint = pm.ls(joint, tr=True)[0]
    control = pm.circle(normal=(1, 0, 0), radius=radius)[0]
    pm.matchTransform(control, joint)
    offset_transformations(control)
    return control


def offset_transformations(node=None):
    """Transfers rotations to offset parent matrix"""
    transforms = pm.ls(node, tr=True) if node else pm.ls(sl=True, tr=True)
    for transform in transforms:
        if pm.versions.current() > 20190000 or offset_node_override:
            pm.connectAttr(transform.matrix, transform.offsetParentMatrix, force=True)
            pm.disconnectAttr(transform.matrix, transform.offsetParentMatrix)
            pm.setAttr(transform.translate, (0, 0, 0), type='float3')
            pm.setAttr(transform.rotate, (0, 0, 0), type='float3')
        else:
            offset_node = pm.group(transform)
            pm.setAttr(offset_node.rotate, pm.getAttr(transform.rotate), type='float3')
            pm.setAttr(transform.translate, (0, 0, 0), type='float3')
            pm.setAttr(transform.rotate, (0, 0, 0), type='float3')
            pm.makeIdentity(offset_node, apply=True, translate=True)


def get_selected_joints():
    return pm.ls(sl=True, type=pm.nodetypes.Joint)


def create_control_from_selected_joints(radius=1.0, point=True, orient=False):
    for joint in get_selected_joints():
        control = pm.circle(normal=(1, 0, 0), radius=radius)[0]
        pm.matchTransform(control, joint)
        if point:
            pm.pointConstraint(control, joint, maintainOffset=True)
        if orient:
            pm.orientConstraint(control, joint, maintainOffset=True)


def get_joint_and_control(verbose=False):
    # returns a joint and a control if only a single joint and control are selected
    selection = pm.ls(sl=True, tr=True)
    if len(selection) == 2:
        joint = next((x for x in selection if type(x) == pm.nodetypes.Joint), None)
        control = next((x for x in selection if type(x) != pm.nodetypes.Joint), None)
        if verbose:
            print(f'Joint: {joint.name()}\nControl: {control.name()}')
        return joint, control
    else:
        return None, None


def snap_and_align_control_to_joint():
    joint, control = get_joint_and_control()
    if joint and control:
        pm.matchTransform(control, joint)
        pm.select(control)
    else:
        pm.warning("Please select joint and control")


def constrain_joint_to_control(constraint_type, maintain_offset=True):
    joint, control = get_joint_and_control()
    if joint and control:
        if constraint_type == ConstraintType.point:
            pm.pointConstraint(control, joint, maintainOffset=maintain_offset)
        elif constraint_type == ConstraintType.orient:
            pm.orientConstraint(control, joint, maintainOffset=maintain_offset)
        elif constraint_type == ConstraintType.parent:
            pm.parentConstraint(control, joint, maintainOffset=maintain_offset)
    else:
        pm.warning("Please select joint and control")

def move_and_parent_constraint_control_to_joint(maintain_offset=True):
    joint, control = get_joint_and_control()
    if joint and control:
        pm.matchTransform(control, joint)
        pm.parentConstraint(joint, control, maintainOffset=maintain_offset)
    else:
        pm.warning("Please select joint and control")

def set_visible(transform, value=True):
    pm.setAttr(transform.visibility, value)
    pm.setAttr(transform.castsShadows, value)
    pm.setAttr(transform.receiveShadows, value)
    pm.setAttr(transform.primaryVisibility, value)
    pm.setAttr(transform.visibleInReflections, value)
    pm.setAttr(transform.visibleInRefractions, value)

def create_proximity_constraint():
    joint, control = get_joint_and_control()
    if joint and control:
        proximity_mesh, _ = pm.polyPlane(axis=[0, 1, 0], width=.25, height=.25, name='proximityTarget', sx=1, sy=1)
        set_visible(proximity_mesh, False)
        pm.matchTransform(proximity_mesh, joint)
        pm.parent(proximity_mesh, joint)
        import maya.internal.common.cmd.base
        pm.select(proximity_mesh, control)
        maya.internal.common.cmd.base.executeCommand('proximitypin.cmd_create')
