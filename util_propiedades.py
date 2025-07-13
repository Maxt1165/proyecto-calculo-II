import bpy

class CalcBlenderProperties(bpy.types.PropertyGroup ):
    superficie_funcion : bpy.props.StringProperty(name="Función z =",description="Expresión matemática z=f(x,y)")
    superficie_x_min : bpy.props.FloatProperty(name="X Min", default=-5.0)
    superficie_x_max : bpy.props.FloatProperty(name="X Max", default=5.0)
    superficie_y_min : bpy.props.FloatProperty(name="Y Min", default=-5.0)
    superficie_y_max : bpy.props.FloatProperty(name="Y Max", default=5.0)
    superficie_resolucion : bpy.props.IntProperty(name="Resolución",    description="Cantidad de subdivisiones",default=20, min=3, max=100)# type: ignore

    punto_gradiente_x : bpy.props.FloatProperty(name="X₀", description="Punto X donde evaluar el gradiente", default=0.0)
    punto_gradiente_y : bpy.props.FloatProperty(name="Y₀", description="Punto Y donde evaluar el gradiente", default=0.0)
    
    #description="Vista previa de la función validada",
    function_preview : bpy.props.StringProperty(name="Vista previa", default="")
    gradiente_preview : bpy.props.StringProperty(name="∇f",default="",description="Vista previa del gradiente calculado")

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