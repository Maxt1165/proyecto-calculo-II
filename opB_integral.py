import bpy
from . import logica_integral_calculo

class CB_OT_VisualizarIntegral(bpy.types.Operator):
    bl_idname = "calcblender.visualizar_integral"
    bl_label = "Calcular Integral Definida"
    bl_description = "Calcula la integral definida de z=f(x,y) sobre un dominio rectangular"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.calcblender_props
        expr = props.superficie_funcion
        a, b = props.integral_x_min, props.integral_x_max
        c, d = props.integral_y_min, props.integral_y_max

        if not expr:
            self.report({'ERROR'}, "Debes ingresar una función z = f(x,y)")
            return {'CANCELLED'}

        resultado = logica_integral_calculo.calcular_integral_definida(expr, a, b, c, d)

        if resultado is not None:
            props.integral_preview = f"∬_D f(x,y) dxdy ≈ {resultado:.4f}"
            self.report({'INFO'}, "Integral calculada con éxito")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Error al calcular la integral")
            return {'CANCELLED'}
