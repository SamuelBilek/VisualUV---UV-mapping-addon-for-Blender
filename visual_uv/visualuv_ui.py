import bpy

class VisualUVPanel():
    def draw_ui(self, layout, context, is_uv):
        if not context.selected_objects:
            layout.label(text='No object selected')
            return
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                layout.label(text='Some selected objects are not MESH objects')
                return
            if not obj.data.uv_layers.active:
                layout.label(text='Some selected objects do not have an active UV layer')
                return
        obj = context.selected_objects[0]
        visualuv = obj.visualuv
        operation_box = None

        #Hide texture button
        toggle_text = 'Hide Texture' if visualuv.checker_texture else 'Show Texture'
        toggle_icon = 'TEXTURE' if visualuv.checker_texture else 'MESH_PLANE'

        texture_box = layout.box()
        texture_container = texture_box.row()
        texture_container.operator('visualuv.toggle_texture', text=toggle_text, icon=toggle_icon)
        texture_container.scale_y = 1.5

        layout.separator(factor=0.1)

        toggle_text = 'Enable Stretching' if visualuv.operation != 'UV_STRETCHING' else 'Disable Stretching'
        toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_STRETCHING' else 'HIDE_ON'

        enable_box = layout.box()
        enable_container = enable_box.row()
        enable_container.operator('visualuv.toggle_stretching', text=toggle_text, icon=toggle_icon)
        enable_container.scale_y = 1.5
        if visualuv.operation == 'UV_STRETCHING':
            operation_box = enable_box

        layout.separator(factor=0.1)

        # UV normals button
        toggle_text = 'Enable UV Normals' if visualuv.operation != 'UV_NORMALS' else 'Disable UV Normals'
        toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_NORMALS' else 'HIDE_ON'

        enable_box = layout.box()
        enable_container = enable_box.row()
        enable_container.operator('visualuv.toggle_normals', text=toggle_text, icon=toggle_icon)
        enable_container.scale_y = 1.5
        if visualuv.operation == 'UV_NORMALS':
            operation_box = enable_box

        layout.separator(factor=0.1)

        # UV overlapping button
        if obj.mode == 'EDIT' and not bpy.context.tool_settings.use_uv_select_sync:
            toggle_text = 'Enable UV Overlapping' if visualuv.operation != 'UV_OVERLAP' else 'Disable UV Overlapping'
            toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_OVERLAP' else 'HIDE_ON'

            enable_box = layout.box()
            enable_container = enable_box.row()
            enable_container.operator('visualuv.toggle_overlap', text=toggle_text, icon=toggle_icon)
            enable_container.scale_y = 1.5
            if visualuv.operation == 'UV_OVERLAP':
                operation_box = enable_box

            layout.separator(factor=0.1)

        # UV island coloring button
        toggle_text = 'Enable Island Coloring' if visualuv.operation != 'UV_ISLANDS' else 'Disable Island Coloring'
        toggle_icon = 'HIDE_OFF' if visualuv.operation == 'UV_ISLANDS' else 'HIDE_ON'

        enable_box = layout.box()
        enable_container = enable_box.row()
        enable_container.operator('visualuv.toggle_islands', text=toggle_text, icon=toggle_icon)
        enable_container.scale_y = 1.5
        if visualuv.operation == 'UV_ISLANDS':
            operation_box = enable_box

        layout.separator(factor=0.1)

        if visualuv.operation == 'NONE' and not visualuv.checker_texture:
            return

        # texture controls
        if visualuv.checker_texture:
            subbox = texture_box.box()
            subbox.template_ID(visualuv, 'image', open='image.open', new='image.new')
            subbox.prop(visualuv, 'texture_scale', text='Texture Scale', slider=True)
            if is_uv:
                subbox.prop(visualuv, 'texture_alpha', text='Texture Alpha', slider=True)
                subbox.prop(visualuv, 'fill_texture', text='Texture Fill')
        
        # current operation controls
        if operation_box:
            if visualuv.operation == 'UV_STRETCHING':
                subbox = operation_box.box()
                subbox.prop(visualuv, 'max_division', text='Stretch Factor', slider=True)     
                subbox.prop(visualuv, 'stretch_type', expand=True)
            elif visualuv.operation == 'UV_ISLANDS':
                subbox = operation_box.box()
                subbox.prop(visualuv, 'hue_multiply', text='Color Variation')

        # refresh options
        refresh_box = layout.box()
        refresh_box.operator('visualuv.update', text='Refresh', icon='FILE_REFRESH')
        refresh_box.prop(visualuv, 'auto_update', text="Auto-Update")
        refresh_box.scale_y = 1.5
        layout.separator(factor=0.1)
        
        # controls for enabling additional features
        main_box = layout.box()
        main_box.prop(visualuv, 'alpha', text='Overlay Opacity', slider=True)
        if is_uv:
            main_box.prop(visualuv, 'overlay_layer', text='Layer', icon='NODE_COMPOSITING')
        main_box.prop(visualuv, 'show_3D', text='Render 3D Viewport', icon='VIEW3D')
        main_box.prop(visualuv, 'show_2D', text='Render UV Editor', icon='UV')
        if not is_uv:
            main_box.prop(visualuv, 'show_wire', text='Wireframe', icon='SHADING_WIRE')
            main_box.prop(visualuv, 'backface_culling', text='Backface Culling', icon='AXIS_SIDE')
        layout.separator(factor=0.1)

        # change color box
        if visualuv.operation != 'NONE':
            color_box = layout.box()
            color_box.prop(visualuv, 'enable_color_change', text='Color Change', icon='BRUSH_DATA')
            if visualuv.enable_color_change:
                color_box.prop(visualuv, 'hue_shift', text='Hue Shift', slider=True)
                color_box.prop(visualuv, 'saturation', text='Saturation', slider=True)
                color_box.prop(visualuv, 'value', text='Value', slider=True)
                color_box.separator(factor=0.1)
        layout.separator(factor=0.1)

        if is_uv:
            return

        # change location box
        location_box = layout.box()
        location_box.prop(visualuv, 'enable_position_change', text='Position Change', icon='OBJECT_ORIGIN')
        if visualuv.enable_position_change:
            location_box.prop(visualuv, 'location_offset', text='Location Offset')
            location_box.separator(factor=0.1)
        layout.separator(factor=0.1)

        # explosion view box
        explosion_box = layout.box()
        explosion_box.prop(visualuv, 'enable_explosion_view', text='Explosion View', icon='MOD_EXPLODE', toggle=True)
        if visualuv.enable_explosion_view:
            explosion_box.prop(visualuv, 'explosion_offset', text='Explosion Offset', slider=False)
            explosion_box.separator(factor=0.1)
        layout.separator(factor=0.1)

class VISUALUV_PT_3d_view(bpy.types.Panel, VisualUVPanel):
    bl_label = "VisualUV Overlays"
    bl_idname = "VISUALUV_PT_uv_tool_menu3d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VisualUV'

    def draw(self, context):
        layout = self.layout
        self.draw_ui(layout, context, False)

class VISUALUV_PT_2d_view(bpy.types.Panel,VisualUVPanel):
    bl_label = "VisualUV Overlays"
    bl_idname = "VISUALUV_PT_uv_tool_menu2d"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'VisualUV'

    def draw(self, context):
        layout = self.layout
        self.draw_ui(layout, context, True)
