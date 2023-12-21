import pymel.core as pm

from typing import Sequence, Union, Optional


def set_translation_keyframe(transform: pm.nodetypes.Transform, frames: Union[int, float, str, Sequence],
                             value: Sequence[float]):
    """
    Set a translation keyframe on a transform or set of transforms
    @param transform:
    @param frames: assumes keyframes, can use form '#sec' for str format
    @param value:
    """
    pm.setKeyframe(transform, attribute='translateX', time=frames, value=value[0])
    pm.setKeyframe(transform, attribute='translateY', time=frames, value=value[1])
    pm.setKeyframe(transform, attribute='translateZ', time=frames, value=value[2])


def set_rotation_keyframe(transform: pm.nodetypes.Transform, frames: Union[int, float, str, Sequence],
                          value: Sequence[float]):
    """
    Set a rotation keyframe on a transform or set of transforms
    @param transform:
    @param frames: assumes keyframes, can use form '#sec' for str format
    @param value:
    """
    pm.setKeyframe(transform, attribute='rotateX', time=frames, value=value[0])
    pm.setKeyframe(transform, attribute='rotateY', time=frames, value=value[1])
    pm.setKeyframe(transform, attribute='rotateZ', time=frames, value=value[2])


def set_scale_keyframe(transform: pm.nodetypes.Transform, frames: Union[int, float, str, Sequence],
                       value: Sequence[float]):
    """
    Set a scale keyframe on a transform or set of transforms
    @param transform:
    @param frames: assumes keyframes, can use form '#sec' for str format
    @param value:
    """
    pm.setKeyframe(transform, attribute='scaleX', time=frames, value=value[0])
    pm.setKeyframe(transform, attribute='scaleY', time=frames, value=value[1])
    pm.setKeyframe(transform, attribute='scaleZ', time=frames, value=value[2])


def clear_keyframes(transform: pm.nodetypes.Transform, start: Optional[float] = None, end: Optional[float] = None):
    """
    Removes keyframes on a transform within an inclusive range
    If not passed, all keyframes are cleared
    @param transform:
    @param start:
    @param end:
    """
    pm.cutKey(transform, time=f'{start if start else ""}:{end if end else ""}')
