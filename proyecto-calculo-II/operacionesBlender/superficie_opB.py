#Creación de superficies

#Dada una función matemática z = f(x, y), generar una una malla (grid) que represente esa superficie en el espacio 3D.
"""PASOS
1. Definir la función: El usuario ingresa una cadena (string) con la expresión matemática, por ejemplo: `"x**2 + y**2"`.
2. Definir el dominio: Rango para `x` y `y` (por ejemplo, `x` de -5 a 5, `y` de -5 a 5) y la resolución (número de puntos).
3. Evaluar la función: Para cada punto `(x, y)` en el dominio, calcular `z = f(x, y)`.
4. Crear la malla: Construir una malla de vértices y caras (quadrados o triángulos) que represente la superficie.
5. Añadir el objeto a la escena de Blender """

import bpy
from ..logica import surface_generator

class CALCBLENDER_OT_CreateSurface(bpy.types.Operator):
    bl_idname = "calcblender.create_surface"
    bl_label = "Crear Superficie"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        props = context.scene.calcblender_props
        
        try:
            # Crear superficie
            obj = surface_generator.create_surface(
                expression=props.surface_function,
                x_domain=(props.surface_x_min, props.surface_x_max),
                y_domain=(props.surface_y_min, props.surface_y_max),
                resolution=props.surface_resolution
            )
            
            # Posicionar en cursor 3D
            obj.location = context.scene.cursor.location
            
            # Seleccionar y activar
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Agregar modificador para suavizado
            obj.modifiers.new(name="Suavizado", type='SMOOTH')
            obj.data.use_auto_smooth = True
            
            self.report({'INFO'}, f"Superficie creada: {obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}