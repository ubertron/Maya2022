import pymel.core as pm

from pathlib import Path
from typing import Optional, List, Tuple


FILE_TEXTURE_NODES: List[pm.nodetypes.File] = pm.ls(type=pm.nodetypes.File)
LAMBERT_SHADER_NODES: List[pm.nodetypes.Lambert] = pm.ls(type=pm.nodetypes.Lambert)


def apply_shader(shading_group, obj_list: Optional[pm.nodetypes.Transform] = None):
    """
    Apply a shader to a collection of Transforms
    @param shading_group:
    @param obj_list:
    """
    pm.sets(shading_group, edit=True, forceElement=pm.ls(obj_list) if obj_list else pm.ls(sl=True))


def lambert_shader(name: str, color: Optional = None):
    """
    Create a Lambert shader node
    @param name:
    @param color:
    @return:
    """
    shader = pm.shadingNode('lambert', asShader=True, name=f'{name}Shader')
    shading_group = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{name}SG')
    pm.connectAttr(shader.outColor, shading_group.surfaceShader)

    if color:
        set_diffuse_color(shader, color)

    return shader, shading_group


def get_shading_group_from_shader(shader):
    """
    Get the shading group for a shader
    @param shader:
    @return:
    """
    shadingGroups = pm.listConnections(shader, type='shadingEngine')

    if shadingGroups:
        return shadingGroups[0]


def lambert_file_texture_shader(texture_path: Path, name=None, check_existing: bool = True) -> Tuple:
    """
    Create a Lambert shader with a file texture node
    @param texture_path:
    @param name:
    @param check_existing:
    @return:
    """
    assert texture_path.exists(), f'Path not found: {texture_path}'
    name = name if name else texture_path.stem
    shader_name = f'{name}Shader'

    if check_existing:
        output_shader = next((x for x in LAMBERT_SHADER_NODES if x.name() == shader_name), None)
        if output_shader:
            return output_shader, get_shading_group_from_shader(output_shader)

    output_shader, shading_group = lambert_shader(name)
    file_node = file_texture_node(texture_path, name)
    pm.connectAttr(file_node.outColor, output_shader.color)

    return output_shader, shading_group


def set_diffuse_color(shader, color: Tuple[float]):
    """
    Set the diffuse value of a shader
    @param shader:
    @param color:
    """
    pm.setAttr(shader.colorR, color[0])
    pm.setAttr(shader.colorG, color[1])
    pm.setAttr(shader.colorB, color[2])


def file_texture_node(texture_path: Path, name: Optional[str] = None, check_existing: bool = True):
    """
    create a file texture node with a texture placement node
    @param texture_path:
    @param name:
    @param check_existing:
    @return:
    """
    name = name if name else texture_path.stem
    file_node_name = f'{name}File'

    if check_existing:
        file_node = next((x for x in FILE_TEXTURE_NODES if x.name() == file_node_name), None)
        if file_node:
            return file_node

    file_node = pm.shadingNode('file', asTexture=True, name=file_node_name)
    placement_node = pm.shadingNode('place2dTexture', asUtility=True, name=f'{name}Place2dTexture')
    pm.setAttr(file_node.fileTextureName, texture_path, type='string')
    pm.connectAttr(placement_node.outUV, file_node.uvCoord)
    pm.connectAttr(placement_node.coverage, file_node.coverage)
    pm.connectAttr(placement_node.mirrorU, file_node.mirrorU)
    pm.connectAttr(placement_node.mirrorV, file_node.mirrorV)
    pm.connectAttr(placement_node.noiseUV, file_node.noiseUV)
    pm.connectAttr(placement_node.offset, file_node.offset)
    pm.connectAttr(placement_node.outUvFilterSize, file_node.uvFilterSize)
    pm.connectAttr(placement_node.repeatUV, file_node.repeatUV)
    pm.connectAttr(placement_node.rotateFrame, file_node.rotateFrame)
    pm.connectAttr(placement_node.rotateUV, file_node.rotateUV)
    pm.connectAttr(placement_node.stagger, file_node.stagger)
    pm.connectAttr(placement_node.translateFrame, file_node.translateFrame)
    pm.connectAttr(placement_node.vertexCameraOne, file_node.vertexCameraOne)
    pm.connectAttr(placement_node.vertexUvOne, file_node.vertexUvOne)
    pm.connectAttr(placement_node.vertexUvTwo, file_node.vertexUvTwo)
    pm.connectAttr(placement_node.vertexUvThree, file_node.vertexUvThree)
    pm.connectAttr(placement_node.wrapU, file_node.wrapU)
    pm.connectAttr(placement_node.wrapV, file_node.wrapV)

    return file_node


