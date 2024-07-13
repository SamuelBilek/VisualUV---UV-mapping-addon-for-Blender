import bpy
from bpy.props import BoolProperty, FloatVectorProperty, FloatProperty, EnumProperty, PointerProperty, IntProperty


class VISUALUV_ObjectProperties(bpy.types.PropertyGroup):
    enabled : BoolProperty()
    auto_update : BoolProperty(
        default=True,
        update=lambda self, context: self.update_func(),
        description="Toggle the Auto-Update feature"
    )
    backface_culling : BoolProperty(
        description="Turn on to cull backfaces"
    )
    show_wire : BoolProperty(
        default=True,
        description="Display wireframe in Edit-Mode, with seams, selected vertices, edges, and faces",
        update=lambda self, context: self.update_func()
    )
    alpha : FloatProperty(
        default=0.75,
        max=1.0,
        min=0.0,
        description="Tweak the overlay's opacity"
    )
    recalculate : BoolProperty()
    overlap_recalculate : BoolProperty()
    show_3D : BoolProperty(
        default=True,
        description="Display the overlay in the 3D Viewport"
    )
    show_2D : BoolProperty(
        default=True,
        description="Display the overlay in the UV Editor"
    )
    overlay_layer : IntProperty(
        default=1,
        description="Move the overlay between background and foreground of the UV Editor",
        min=0,
        max=2
    )
    enable_position_change : BoolProperty(
        description="Enable for the overlay's position manipulation"
    )
    enable_color_change : BoolProperty(
        description="Enable for the overlay's color manipulation"
    )
    enable_explosion_view : BoolProperty(
        description="Enable for separating and offsetting the overlay by individual UV islands",
        update=lambda self, context: self.update_func()
    )
    checker_texture : BoolProperty(
        default=False,
        update=lambda self, context: self.update_func()
    )
    fill_texture : BoolProperty(
        default=True,
        description="Fill the whole UV square with the selected texture of an active object"
    )
    image : PointerProperty(name='Image', type=bpy.types.Image)

    texture_scale : FloatProperty(
        default=1.0,
        soft_max=2.0,
        min=0.01,
        description="Tweak the texture's scale"
    )
    texture_alpha : FloatProperty(
        default=1.0,
        max=1.0, 
        min=0.0,
        description="Tweak the texture's opacity in the UV Editor"
    )
    max_division : FloatProperty(
        default=2.0,
        min=1.01,
        soft_max=5.0,
        description="Tweak the stretching sensitivity. Lower factor means higher sensitivity"
    )
    hue_shift : FloatProperty(
        default=0.0,
        max=1.0, 
        min=0.0,
        description="Tweak the overlay's color hue"
    )
    hue_multiply : FloatProperty(
        default=1.0,
        min=1.0,
        description="Change the color variation of UV islands"
    )
    saturation : FloatProperty(
        default=1.0,
        max=1.0,
        min=0.0,
        description="Tweak the overlay's color saturation"
    )
    value : FloatProperty(
        default=0.8,
        max=1.0, 
        min=0.0,
        description="Tweak the overlay's color value"
    )
    explosion_offset : FloatProperty(
        default=0.0,
        min=0.0,
        description="Tweak the offset of the explosion"
    )
    location_offset : FloatVectorProperty(
        subtype='XYZ',
        description="Tweak the overlay's position"
    )
    operation : EnumProperty(
        items=[
            ('NONE', "None", "", 1),
            ('UV_STRETCHING', "Stretching", "", 2),
            ('UV_ISLANDS', "Islands", "", 3),
            ('UV_NORMALS', "Normals", "", 4),
            ('UV_OVERLAP', "Overlap", "", 5)
        ],
        default='NONE',
        update=lambda self, context: self.update_func()
    )
    stretch_type : EnumProperty(
        items=[
            ('ANGLES', "Angles", "Stretching between angles of the UV map and the original model", 1), 
            ('AREA', "Area", "Stretching between the relative areas of the UV map and the original model", 2), 
            ('EDGE_LENGTH', "Edge length", "Stretching between the relative edge lengths of the UV map and the original model", 3)
        ], 
        default='ANGLES',
        update=lambda self, context: self.update_func()
    )

    def update_func(self):
        value = getattr(self, 'operation') != 'NONE' or getattr(self, 'checker_texture')
        setattr(self, 'recalculate', value)
        setattr(self, 'enabled', value)


class VISUALUV_WindowManagerProperties(bpy.types.PropertyGroup):
    select_overlap : BoolProperty(default=False)
    