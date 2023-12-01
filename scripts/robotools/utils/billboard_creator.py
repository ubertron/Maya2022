import pymel.core as pm
from PIL import Image

from typing import Optional
from pathlib import Path

from robotools import material_utils
from core.enums import Axis
from robotools.widgets import xp_widget


def create_billboard(image_path: Path, width: float = 10.0, axis: Axis = Axis.y,
                     name: Optional[str] = None) -> pm.nodetypes.Transform:
    """
    Create a plane with a texture applied
    @param image_path:
    @param width:
    @param axis:
    @param name:
    @return:
    """
    assert image_path.exists(), f'Path not found: {image_path}'

    with Image.open(image_path.as_posix()) as im:
        image_width, image_height = im.size

    height = width * image_height / image_width
    billboard, _ = pm.polyPlane(width=width, height=height, axis=axis.value, name=name, subdivisionsX=1,
                                subdivisionsY=1)
    texture_shader, texture_shader_sg = material_utils.lambert_file_texture_shader(texture_path=image_path,
                                                                                   check_existing=True)
    material_utils.apply_shader(shading_group=texture_shader_sg, obj_list=billboard)

    return billboard


class BillboardCreator(xp_widget.XPWidget):
    def __init__(self):
        super(BillboardCreator, self).__init__(title='Billboard Creator', margin=4, spacing=4)

