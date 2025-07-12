#Creación de superficies
import bpy
#Dada una función matemática z = f(x, y), generar una una malla (grid) que represente esa superficie en el espacio 3D.
"""PASOS
1. Definir la función: El usuario ingresa una cadena (string) con la expresión matemática, por ejemplo: "x**2 + y**2".
2. Definir el dominio: Rango para x y y (por ejemplo, x de -5 a 5, y de -5 a 5) y la resolución (número de puntos).
3. Evaluar la función: Para cada punto (x, y) en el dominio, calcular z = f(x, y).
4. Crear la malla: Construir una malla de vértices y caras (quadrados o triángulos) que represente la superficie.
5. Añadir el objeto a la escena de Blender """
from ..logica import superficie_generar

class CrearSuperficies(bpy.types.Operator):
    bl_idname = "visualizador_superficies.crearsuperficie"
    bl_label = "Crear Superficie"
    bl_options = {'REGISTER', 'UNDO'}
    #REGISTER: Hace visible el operador en la UI y permite asignar atajos de teclado.
    #Permite deshacer la acción con Ctrl+Z.

    @classmethod
    #Verifica si el operador puede ejecutarse en el contexto actual
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    #carga las propiedades guardadas (como la función matemática y rangos)
    # desde la escena de Blender para usarlas en los cálculos.
    #Retorna {'FINISHED'} si tiene éxito.
    def execute(self, context):
        props = context.scene.calcblender_props
        
        try:
            # Crear superficie
            obj = superficie_generar.create_surface(
                expression=props.superficie_funcion,
                x_domain=(props.superficie_x_min, props.superficie_x_max),
                y_domain=(props.superficie_y_min, props.superficie_y_max),
                resolution=props.superficie_resolution
            )
          # Posicionar el objeto en la ubicación del cursor 3D de Blender
            obj.location = context.scene.cursor.location  # Usa la posición actual del cursor como origen

            # Deseleccionar todos los objetos y activar el nuevo
            bpy.ops.object.select_all(action='DESELECT')  # Limpia la selección actual
            context.view_layer.objects.active = obj       # Establece como objeto activo
            obj.select_set(True)                          # Selecciona el nuevo objeto

            # Aplicar suavizado automático a la superficie
            obj.modifiers.new(name="Suavizado", type='SMOOTH')  # Añade modificador de suavizado
            obj.data.use_auto_smooth = True                     # Habilita normales suavizadas

            # Notificar éxito en la consola y panel de información
            self.report({'INFO'}, f"Superficie creada: {obj.name}")  # Mensaje de confirmación
            return {'FINISHED'}  # Indica que el operador terminó correctamente

        except Exception as e:  # Manejo de errores
            self.report({'ERROR'}, f"Error: {str(e)}")  # Muestra error en la UI
            return {'CANCELLED'}  # Indica que la operación falló