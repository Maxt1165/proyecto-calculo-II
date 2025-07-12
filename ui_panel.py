import bpy
print("Se importó bpy en el archivo ui_panel")

#from . import gui
"""
class VISUALIZADOR_PT_Panel(bpy.types.Panel):
    bl_label = "Panel de Prueba"
    bl_idname = "VISUALIZADOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Superficies'

    def draw(self, context):
        layout = self.layout
        layout.label(text="GANARON LOS MALOS 🗣️")
        """
#main_panel 
class CALCBLENDER_PT_SurfacePanel(bpy.types.Panel):
    bl_label = "Superficies"
    bl_idname = "CALCBLENDER_PT_SurfacePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CalcBlender'
    bl_context = "objectmode"
    """Se mostrará en el modo objeto (objectmode), dentro del panel lateral de la vista 3D en la pestaña CalcBlender"""
    
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

class CALCBLENDER_PT_GradientePanel(bpy.types.Panel):
    bl_label      = "Gradientes"
    bl_idname     = "CALCBLENDER_PT_GradientePanel"
    bl_parent_id  = "CALCBLENDER_PT_SurfacePanel"   # lo cuelga debajo
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options    = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = context.scene.calcblender_props   # (si usas un PropertyGroup global)

        box = layout.box()
        box.label(text="Visualizar campo ∇f", icon='FORCE_MAGNETIC')

        if obj and "funcion" in obj:
            row = box.row()
            row.prop(props, "superficie_resolution", text="Resol.")  # usa la misma resolución global
            op = box.operator("calcblender.visualizar_gradiente", text="Generar Gradiente")
            op.resolucion = props.superficie_resolution             # pasa la resolución al operador
        else:
            box.label(text="Seleccione una superficie válida", icon='ERROR')


classes = (
    CALCBLENDER_PT_SurfacePanel,
    CALCBLENDER_PT_GradientePanel,   # ← añade el nuevo
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
