import bpy
#from . import gui

class VISUALIZADOR_PT_Panel(bpy.types.Panel):
    bl_label = "Panel de Prueba"
    bl_idname = "VISUALIZADOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Superficies'

    def draw(self, context):
        layout = self.layout
        layout.label(text="GANARON LOS MALOS 🗣️")

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

#Registro del panel CALCBLENDER_PT_SurfacePanel
def register():
    # Registra tu panel principal de superficies
    bpy.utils.register_class(CALCBLENDER_PT_SurfacePanel)
    
    # Registra este panel adicional si lo necesitas
        #bpy.utils.register_class(VISUALIZADOR_PT_Panel)

def unregister():
    # Desregistra en orden inverso
        #bpy.utils.unregister_class(VISUALIZADOR_PT_Panel)
    bpy.utils.unregister_class(CALCBLENDER_PT_SurfacePanel)