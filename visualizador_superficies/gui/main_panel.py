import bpy
print('Se importó bpy en el archivo main_panel')

class CALCBLENDER_PT_SurfacePanel(bpy.types.Panel):
    bl_label = "Superficies"
    bl_idname = "CALCBLENDER_PT_SurfacePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CalcBlender'
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props
        
        # Configuración de superficie
        box = layout.box()
        box.label(text="Crear Superficie", icon='MESH_GRID')
        
        # Entrada de función con validación
        row = box.row()
        row.prop(props, "surface_function", text="z =")
        row.operator("calcblender.validate_function", text="", icon='CHECKMARK')
        
        # Controles de dominio
        grid = box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.prop(props, "surface_x_min", text="X Min")
        grid.prop(props, "surface_x_max", text="X Max")
        grid.prop(props, "surface_y_min", text="Y Min")
        grid.prop(props, "surface_y_max", text="Y Max")
        
        # Resolución con slider
        box.prop(props, "surface_resolution", slider=True)
        
        # Botón de creación
        box.operator("calcblender.create_surface", text="Generar Superficie", icon='ADD')
        
        # Previsualización matemática
        if hasattr(props, 'function_preview'):
            box.label(text=f"Función válida: {props.function_preview}", icon='CON_TRANSFORM')