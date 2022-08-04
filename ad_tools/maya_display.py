import pymel.core as pm

from ad_tools.maya_poly import get_selected_geometry


def toggle_xray(nodes=None):
    for x in pm.ls(nodes) if nodes else get_selected_geometry():
        pm.displaySurface(x, xRay=(not pm.displaySurface(x, xRay=True, query=True)[0]))


def toggle_backface_culling(nodes=None):
    for x in pm.ls(nodes) if nodes else get_selected_geometry():
        value = x.backfaceCulling
        pm.setAttr(value, 3) if pm.getAttr(value) == 0 else pm.setAttr(value, 0)
