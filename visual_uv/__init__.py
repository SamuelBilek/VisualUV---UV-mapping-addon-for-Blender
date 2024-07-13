# VisualUV
# Copyright (C) 2023 Samuel Bílek

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import bpy
from bpy.props import (
    BoolProperty,
    FloatVectorProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
    IntProperty,
)

from .visualuv_ui import VISUALUV_PT_3d_view, VISUALUV_PT_2d_view
from .visualuv_ops import (
    VISUALUV_OT_update,
    VISUALUV_OT_toggle_texture,
    VISUALUV_OT_toggle_stretching,
    VISUALUV_OT_toggle_islands,
    VISUALUV_OT_toggle_normals,
    VISUALUV_OT_toggle_overlap,
    VISUALUV_OT_overlay,
)
from .visualuv_props import VISUALUV_ObjectProperties, VISUALUV_WindowManagerProperties


bl_info = {
    "name": "VisualUV",
    "author": "Samuel Bílek",
    "description": "Adds UV Mapping visualization overlays for objects. \
        Useful for quick texture preview and visualising UV Stretching, Flipped UVs, Overlapped UVs and for coloring individual UV Islands.",
    "blender": (3, 5, 0),
    "version": (1, 0, 0),
    "location": "3D Viewport / UV Editor > Tools > VisualUV",
    "warning": "",
    "category": "Object",
}

classes = (
    VISUALUV_PT_3d_view,
    VISUALUV_PT_2d_view,
    VISUALUV_OT_update,
    VISUALUV_OT_toggle_texture,
    VISUALUV_OT_toggle_stretching,
    VISUALUV_OT_toggle_islands,
    VISUALUV_OT_toggle_normals,
    VISUALUV_OT_toggle_overlap,
    VISUALUV_OT_overlay,
    VISUALUV_ObjectProperties,
    VISUALUV_WindowManagerProperties,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Object.visualuv = PointerProperty(type=VISUALUV_ObjectProperties)
    bpy.types.WindowManager.visualuv = PointerProperty(
        type=VISUALUV_WindowManagerProperties
    )


def unregister():
    del bpy.types.WindowManager.visualuv
    del bpy.types.Object.visualuv

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
