import bpy
print("Se importó bpy en el archivo ui_panel")

"""class VISUALIZADOR_PT_Panel(bpy.types.Panel):
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
    """Se mostrará en el modo objeto, dentro del panel lateral de la vista 3D en la pestaña CalcBlender"""
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props #accede al grupo de propiedades personalizado del proyecto
        # Configuración de superficie: caja principal
        box = layout.box()
        box.label(text="Crear Superficie", icon='MESH_GRID')
        
        # Entrada de función con validación
        box.label(text="Función z = f(x, y):")
        row = box.row()
        row.prop(props, "superficie_funcion", text="z =")
            #row.operator("calcblender.validate_function", text="", icon='CHECKMARK')  # Botón para validar la función
        
        # Controles de dominio
        grid = box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.prop(props, "superficie_x_min", text="X Min")
        grid.prop(props, "superficie_x_max", text="X Max")
        grid.prop(props, "superficie_y_min", text="Y Min")
        grid.prop(props, "superficie_y_max", text="Y Max")
        
        # Resolución con slider
        box.prop(props, "superficie_resolucion", slider=True)
        
        # Botón de creación
        box.operator("visualizador_superficies.crearsuperficie", text="Generar Superficie", icon='ADD')
        
        # Previsualización matemática
        if props.function_preview:
            box.label(text=f"Función válida: {props.function_preview}", icon='CON_TRANSFORM')


# Subpanel para visualización de gradientes
class CALCBLENDER_PT_GradientePanel(bpy.types.Panel):
    bl_label      = "Gradientes"
    bl_idname     = "CALCBLENDER_PT_GradientePanel"
    bl_parent_id  = "CALCBLENDER_PT_SurfacePanel"   # lo cuelga debajo
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options    = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props   # (si usas un PropertyGroup global)
        obj = context.active_object

        box = layout.box()
        box.label(text="Visualizar campo ∇f", icon='FORCE_MAGNETIC')

        if obj and "funcion" in obj:
            row = box.row()
            row.prop(props, "superficie_resolucion", text="Resolución")
            op = box.operator("calcblender.visualizar_gradiente", text="Generar Gradiente")
            op.resolucion = props.superficie_resolucion
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
