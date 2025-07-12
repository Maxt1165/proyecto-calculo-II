import bpy

class CalcBlenderProperties(bpy.types.PropertyGroup):
    superficie_funcion: bpy.props.StringProperty(name="Función z =")
    superficie_x_min: bpy.props.FloatProperty(name="X Min", default=-5)
    superficie_x_max: bpy.props.FloatProperty(name="X Max", default=5)
    superficie_y_min: bpy.props.FloatProperty(name="Y Min", default=-5)
    superficie_y_max: bpy.props.FloatProperty(name="Y Max", default=5)
    superficie_resolution: bpy.props.IntProperty(name="Resolución", default=10, min=3, max=30)
