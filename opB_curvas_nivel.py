import bpy
from bpy.types import Operator
from . import logica_curvas_nivel  # Donde definiste las funciones de cálculo
from math import floor, ceil
from .logica_curvas_nivel import animar_curvas_a_plano

#GENERADOR DE CURVAS DE NIVEL
class CB_OT_CurvasNivel(Operator):
    bl_idname = "calcblender.curvas_nivel"
    bl_label = "Generar Curvas de Nivel"
    bl_description = "Crea curvas de nivel para z = c en la superficie seleccionada"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene and context.scene.calcblender_props.superficie_funcion.strip()

    def execute(self, context):
        props = context.scene.calcblender_props

        try:
            # Preparar niveles enteros dentro del rango visual
            if props.niveles_curvas.strip():
                # Si el usuario escribió niveles manuales, usarlos
                niveles = [float(n.strip()) for n in props.niveles_curvas.split(",") if n.strip()]
            else:
                # Si no escribió nada, usar niveles automáticos desde z_min hasta z_max
                zmin = floor(props.superficie_z_min)
                zmax = ceil(props.superficie_z_max)
                niveles = list(range(zmin, zmax + 1))
            
            if not niveles:
                self.report({'ERROR'}, "No se definieron niveles de curva válidos.")
                return {'CANCELLED'}
                 # 2. Calcular curvas
            
            curvas_por_nivel = logica_curvas_nivel.obtener_curvas_de_nivel(
                expr=props.superficie_funcion,
                x_range=(props.superficie_x_min, props.superficie_x_max),
                y_range=(props.superficie_y_min, props.superficie_y_max),
                resolucion=props.superficie_resolucion,
                niveles=niveles
            )
             # 3. Crear curvas en Blender
            total = 0
            for z, segmentos in curvas_por_nivel.items():
                altura = 0.0 if props.mostrar_curvas_z0 else z
                objetos = logica_curvas_nivel.crear_curva_bezier(segmentos, altura, nombre_base="CurvaNivel")
                total += len(objetos)

            self.report({'INFO'}, f"{total} curvas creadas en niveles {niveles}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error al generar curvas: {e}")
            return {'CANCELLED'}
        
def register():
    bpy.utils.register_class(CB_OT_CurvasNivel)

def unregister():
    bpy.utils.unregister_class(CB_OT_CurvasNivel)
