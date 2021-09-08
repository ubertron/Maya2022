import pymel.core as pm
import random

def get_world_space_translation(transform):
    return pm.xform(transform, query=True, worldSpace=True, rotatePivot=True)

def create_locator(translation, local_scale=0.1):
    locator = pm.spaceLocator()
    pm.setAttr(locator.translate, translation, type='float3')
    pm.setAttr(locator.localScaleX, local_scale)
    pm.setAttr(locator.localScaleY, local_scale)
    pm.setAttr(locator.localScaleZ, local_scale)
    return locator

def create_random_locators(count, scale=2.0, planar=True):
    locators = []
    for i in range(count):
        tx = 0 if planar else random.uniform(0, scale)
        ty = random.uniform(0, scale)
        tz = random.uniform(0, scale)
        locators.append(create_locator((tx, ty, tz)))
    return locators

def set_random_hierarchy(transforms):
    for i, v in enumerate(transforms[1:]):
        pm.parent(v, random.choice(transforms[:i+1]))

def create_random_symmetrical_hierarchy(count, scale):
    root_locator = create_locator((0, random.uniform(0, scale), random.uniform(0, scale)))
    spine = [root_locator]
    limbs = []
    for i in range(count):
        if random.choice([True, False]):
            locator = create_locator((0, random.uniform(0, scale), random.uniform(0, scale)))
            pm.parent(locator, random.choice(spine))
            spine.append(locator)
        else:
            position = [random.uniform(0, scale), random.uniform(0, scale), random.uniform(0, scale)]
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
