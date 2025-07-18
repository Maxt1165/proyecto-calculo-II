import bpy

class CalcBlenderProperties(bpy.types.PropertyGroup ):
    superficie_funcion : bpy.props.StringProperty(name="Función z =",description="Expresión matemática z=f(x,y)") # type: ignore
    superficie_x_min : bpy.props.FloatProperty(name="X Min", default=-5.0) # type: ignore
    superficie_x_max : bpy.props.FloatProperty(name="X Max", default=5.0) # type: ignore
    superficie_y_min : bpy.props.FloatProperty(name="Y Min", default=-5.0) # type: ignore
    superficie_y_max : bpy.props.FloatProperty(name="Y Max", default=5.0) # type: ignore
    superficie_resolucion : bpy.props.IntProperty(name="Resolución",    description="Cantidad de subdivisiones",default=20, min=3, max=100)# type: ignore

    punto_gradiente_x : bpy.props.FloatProperty(name="X₀", description="Punto X donde evaluar el gradiente", default=0.0) # type: ignore
    punto_gradiente_y : bpy.props.FloatProperty(name="Y₀", description="Punto Y donde evaluar el gradiente", default=0.0) # type: ignore
    
    integral_x_min: bpy.props.FloatProperty(name="x min", default=0.0) # type: ignore
    integral_x_max: bpy.props.FloatProperty(name="x max", default=1.0) # type: ignore
    integral_y_min: bpy.props.FloatProperty(name="y min", default=0.0) # type: ignore
    integral_y_max: bpy.props.FloatProperty(name="y max", default=1.0) # type: ignore
    
    #FUNCIONES DE VISUALIZACIÓN DE VALORES
    function_preview : bpy.props.StringProperty(name="Vista previa", default="") # type: ignore
    gradiente_preview : bpy.props.StringProperty(name="∇f",default="",description="Vp: gradiente calculado") # type: ignore
    plano_tangente_preview: bpy.props.StringProperty(name="Plano Tangente", default="", description="Vp: ecuación del plano tangente") # type: ignore
    niveles_curvas : bpy.props.StringProperty(name="Niveles Maximos z", description="Lista separada por comas (ej: 0, 1.5, 3)",default="",) # type: ignore
    mostrar_curvas_z0: bpy.props.BoolProperty(name="Proyectar en z=0",description="Si está activo, las curvas de nivel se mostrarán en z=0",default=False) # type: ignore
    
    integral_preview: bpy.props.StringProperty(name="Resultado", default="", description="Resultado de la integral doble") # type: ignore

# Registro mejorado con manejo de errores
def register():
    try:
        bpy.utils.register_class(CalcBlenderProperties)
        bpy.types.Scene.calcblender_props = bpy.props.PointerProperty(
            type=CalcBlenderProperties
        )
        print("CalcBlender: Propiedades registradas correctamente")
    except Exception as e:
        print(f"CalcBlender Error: {str(e)}")

def unregister():
    try:
        del bpy.types.Scene.calcblender_props
        bpy.utils.unregister_class(CalcBlenderProperties)
        print("CalcBlender: Propiedades desregistradas")
    except:
        pass  # Evitar errores si ya no existen