import pymel.core as pm
import ad_node
import ad_rigging

def create_rig():
    pm.delete(pm.ls('locator*', tr=True))
    pm.delete(pm.ls('joint*', tr=True))
    joint_locators = ad_node.create_random_locators(8, 4.0)
    rig = ad_rigging.create_joints_from_transforms(joint_locators)
    pm.delete(joint_locators)
    locators = ad_rigging.create_locators_from_joints(rig)
    pm.select(locators)

def create_rig_hierarchy():
    pm.delete(pm.ls('locator*', tr=True))
    pm.delete(pm.ls('joint*', tr=True))
    joint_locators = ad_node.create_random_locators(8, 4.0, False)
    ad_node.set_random_hierarchy(joint_locators)
    rig = ad_rigging.create_joints_from_hierarchy(joint_locators[0])
    pm.select(rig)
    ad_rigging.reorient_joints(rig)
    pm.delete(joint_locators)
    locator_hierarchy = ad_rigging.create_locators_from_joints(rig)
    pm.select(locator_hierarchy)

def create_creature_rig(num_joints=8):
    pm.delete(pm.ls('locator*', tr=True))
    pm.delete(pm.ls('joint*', tr=True))
    creature_locators = ad_node.create_random_symmetrical_hierarchy(num_joints, 4.0)
    rig = ad_rigging.create_joints_from_hierarchy(creature_locators)
    pm.delete(creature_locators)
    ad_rigging.reorient_joints(rig)
    pm.select(rig)
