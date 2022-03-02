import pymel.core as pm


def toggle_xray(nodes=None):
    for x in nodes if nodes else pm.ls(sl=True, transforms=True):
        pm.displaySurface(x, xRay=(not pm.displaySurface(x, xRay=True, query=True)[0]))


def toggle_backface_culling(nodes=()):
    for item in pm.ls(sl=True, transforms=True) if not nodes else nodes:
        value = item.backfaceCulling
        pm.setAttr(value, 3) if pm.getAttr(value) == 0 else pm.setAttr(value, 0)
