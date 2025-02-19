#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements transformation functions"""

from __future__ import annotations

# noinspection PyUnresolvedReferences
from kornia.geometry.transform import *

__all__ = [
    "Affine",
    "Hflip",
    "HomographyWarper",
    "PyrDown",
    "PyrUp",
    "Rescale",
    "Resize",
    "Rot180",
    "Rotate",
    "Scale",
    "ScalePyramid",
    "Shear",
    "Translate",
    "Vflip",
    "affine",
    "affine3d",
    "build_laplacian_pyramid",
    "build_pyramid",
    "center_crop",
    "center_crop3d",
    "crop_and_resize",
    "crop_and_resize3d",
    "crop_by_boxes",
    "crop_by_boxes3d",
    "crop_by_indices",
    "crop_by_transform_mat",
    "crop_by_transform_mat3d",
    "elastic_transform2d",
    "get_affine_matrix2d",
    "get_affine_matrix3d",
    "get_perspective_transform",
    "get_perspective_transform3d",
    "get_projective_transform",
    "get_rotation_matrix2d",
    "get_shear_matrix2d",
    "get_shear_matrix3d",
    "get_translation_matrix2d",
    "hflip",
    "homography_warp",
    "homography_warp3d",
    "invert_affine_transform",
    "projection_from_Rt",
    "pyrdown",
    "pyrup",
    "remap",
    "rescale",
    "resize",
    "rot180",
    "rotate",
    "rotate3d",
    "scale",
    "shear",
    "translate",
    "upscale_double",
    "vflip",
    "warp_affine",
    "warp_affine3d",
    "warp_grid",
    "warp_grid3d",
    "warp_perspective",
    "warp_perspective3d",
]

from mon.vision import core

console      = core.console
_current_dir = core.Path(__file__).absolute().parent
