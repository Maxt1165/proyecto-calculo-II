import bpy

class CalcBlenderProperties(bpy.types.PropertyGroup ):
    superficie_funcion : bpy.props.StringProperty(name="Función z =",description="Expresión matemática z=f(x,y)")# type: ignore
    superficie_x_min : bpy.props.FloatProperty(name="X Min", default=-5.0)# type: ignore
    superficie_x_max : bpy.props.FloatProperty(name="X Max", default=5.0)# type: ignore
    superficie_y_min : bpy.props.FloatProperty(name="Y Min", default=-5.0)# type: ignore
    superficie_y_max : bpy.props.FloatProperty(name="Y Max", default=5.0)# type: ignore
    superficie_resolucion : bpy.props.IntProperty(name="Resolución",    description="Cantidad de subdivisiones",default=20, min=3, max=100)# type: ignore

    function_preview : bpy.props.StringProperty(# type: ignore
        name="Vista previa", 
        description="Vista previa de la función validada",
        default="",
        options={'HIDDEN'}
    )

def register():
    bpy.utils.register_class(CalcBlenderProperties)
    bpy.types.Scene.calcblender_props : bpy.props.PointerProperty(type=CalcBlenderProperties)# type: ignore

def unregister():
    del bpy.types.Scene.calcblender_props
    bpy.utils.unregister_class(CalcBlenderProperties)
