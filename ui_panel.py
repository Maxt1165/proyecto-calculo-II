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
        row = box.row(align=True)
        row.prop(props, "superficie_funcion", text="z =")
            #row.operator("calcblender.validate_function", text="", icon='CHECKMARK')  # Botón para validar la función
        
        # Controles de dominio
        grid = box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.prop(props, "superficie_x_min", text="X Min")
        grid.prop(props, "superficie_x_max", text="X Max")
        grid.prop(props, "superficie_y_min", text="Y Min")
        grid.prop(props, "superficie_y_max", text="Y Max")
        # NUEVO: límites visuales para Z
        grid.prop(props, "superficie_z_min", text="Z Min")
        grid.prop(props, "superficie_z_max", text="Z Max")
        
        # Resolución con slider
        box.prop(props, "superficie_resolucion", slider=True)
        
        # Botón de creación
        box.operator("visualizador_superficies.crearsuperficie", text="Generar Superficie", icon='ADD')
        
        # Previsualización matemática
        if props.function_preview:
            box.label(text=f"Función válida: {props.function_preview}", icon='CON_TRANSFORM')


#Subpanel para visualización de gradientes y planos tangentes
class CALCBLENDER_PT_GradientePanel(bpy.types.Panel):
    bl_label      = "Gradientes"
    bl_idname     = "CALCBLENDER_PT_GradientePanel"
    bl_parent_id  = "CALCBLENDER_PT_SurfacePanel"   # lo cuelga debajo
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options    = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props  # (si usas un PropertyGroup global)
        obj = context.active_object

        box = layout.box()
        box.label(text="Evaluar ∇f en punto (x₀, y₀)") 

        row = box.row(align=True)
        row.prop(props, "punto_gradiente_x", text="x₀")
        row.prop(props, "punto_gradiente_y", text="y₀")

        if obj and "funcion" in obj:
             # Botón para generar el vector gradiente
            box.operator("calcblender.visualizar_gradiente", text="Mostrar ∇f", icon='CON_ROTLIKE')
            # Botón para generar el plano tangente
            box.operator("calcblender.plano_tangente", text="Mostrar Plano Tangente", icon='MESH_PLANE')
        else:
            box.label(text="Seleccione una superficie válida", icon='ERROR')
            
        if props.gradiente_preview:
            box.separator()
            box.label(text=props.gradiente_preview, icon='INFO')

        if props.plano_tangente_preview:
            box.separator()
            box.label(text="Plano tangente:", icon='MESH_PLANE')
            box.label(text=props.plano_tangente_preview)

#subPanel para curvas de nivel
class CALCBLENDER_PT_CurvasNivelPanel(bpy.types.Panel):
    bl_label = "Curvas de Nivel"
    bl_idname = "CALCBLENDER_PT_CurvasNivelPanel"
    bl_parent_id = "CALCBLENDER_PT_SurfacePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props

        box = layout.box()
        box.label(text="Curvas de Nivel", icon="RNDCURVE")

        # Campo: función z = f(x, y)
        if not props.superficie_funcion.strip():
            box.label(text="⚠ Ingrese una función válida", icon="ERROR")
        else:
            box.label(text=f"f(x,y) = {props.superficie_funcion.strip()}", icon="INFO")
        
        # Propiedades: nivel z mínimo y máximo
        box.prop(props, "niveles_curvas", text="Niveles z (opcional)")
        box.prop(props, "superficie_resolucion", text="Resolución")
        
        # Validación visual
        if not props.superficie_funcion.strip():
            box.label(text="Ingrese una función válida", icon="ERROR")
        # Botón para mostrarlas en z=0
        box.prop(props, "mostrar_curvas_z0",text="Proyectar en z = 0")
        # Botón para generar curvas de nivel
        box.operator("calcblender.curvas_nivel", text="Generar Curvas", icon="OUTLINER_OB_CURVE")
        
class CALCBLENDER_PT_IntegralPanel(bpy.types.Panel):
    bl_label = "Integrales Dobles"
    bl_idname = "CALCBLENDER_PT_IntegralPanel"
    bl_parent_id = "CALCBLENDER_PT_SurfacePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.calcblender_props
        obj = context.active_object

        box = layout.box()
        box.label(text="Evaluar ∬ f(x,y) dxdy")

        grid = box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.prop(props, "integral_x_min", text="x₁")
        grid.prop(props, "integral_x_max", text="x₂")
        grid.prop(props, "integral_y_min", text="y₁")
        grid.prop(props, "integral_y_max", text="y₂")

        box.operator("calcblender.visualizar_integral", text="Calcular Integral", icon='AXIS_TOP')

        if props.integral_preview:
            box.label(text=props.integral_preview, icon='INFO')

classes = (
    CALCBLENDER_PT_SurfacePanel,
    CALCBLENDER_PT_GradientePanel,
    CALCBLENDER_PT_CurvasNivelPanel,
    CALCBLENDER_PT_IntegralPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
