#Creación de superficies
"""Propósito:
Definir un operador personalizado de Blender que genera una malla 3D a partir de una función 
z=f(x,y), utilizando los parámetros definidos en la interfaz del usuario (función, dominio y resolución)."""
import bpy
print("Se importó bpy en el archivo superficie_opB.py")
#Dada una función matemática z = f(x, y), generar una una malla (grid) que represente esa superficie en el espacio 3D.

from . import logica_superficie_generar #contiene a la función crear_superficie
print("Se importó superficie_generar en el archivo opB_superficie.py")

class CALCBLENDER_OT_CrearSuperficie(bpy.types.Operator):
    bl_idname = "visualizador_superficies.crearsuperficie" #Nombre interno del operador
    bl_label = "Crear Superficie"
    bl_options = {'REGISTER', 'UNDO'}
    #REGISTER: Hace visible el operador en la UI /permite asignar atajos de teclado.
    #Permite deshacer la acción con Ctrl+Z.

    @classmethod
    #Verifica si el operador puede ejecutarse 
    def poll(cls, contexto):
        return contexto.mode == 'OBJECT'

    #METODO EJECUTABLE CUANDO EL USUARIO DA CLIC EN CREAR SUPERFICIE
    """carga las propiedades guardadas (función matemática y rangos)
    desde Blender para usarlas en cálculos"""
    def ejecutable_crearSuperficie(self, context):
        #accede a las propiedades personalizadas de Blender
        props = context.scene.calcblender_props
        
        try:
            # Crear superficie: paso de parámetros
            objSuperficie = logica_superficie_generar.crear_superficie(
                expresion=props.superficie_funcion,
                x_dominio=(props.superficie_x_min, props.superficie_x_max),
                y_dominio=(props.superficie_y_min, props.superficie_y_max),
                resolucion=props.superficie_resolution
            )
            """# En el método execute(), después de crear la superficie:
            obj["funcion"] = props.surface_function  # Guardar función como propiedad"""

          # Posicionar el objeto en donde esté el cursor 3D de Blender
            objSuperficie.location = context.scene.cursor.location  # Usa la posición actual del cursor como origen
            
            #Coloca la superficie en la posición del cursor 3D
            bpy.ops.object.select_all(action='DESELECT')  # Limpia la selección actual
            context.view_layer.objects.active = objSuperficie       # Establece como objeto activo
            objSuperficie.select_set(True)                          # Selecciona el nuevo objeto

            # Aplicar suavizado automático a la superficie
            objSuperficie.modifiers.new(name="Suavizado", type='SMOOTH')  # Añade modificador de suavizado
            objSuperficie.data.use_auto_smooth = True                     # Habilita normales suavizadas

            # Notificar éxito en la consola y panel de información
            self.report({'INFO'}, f"Superficie creada: {objSuperficie.name}")  # Mensaje de confirmación
            return {'FINISHED'}  # Indica que el operador terminó correctamente

        except Exception as e:  # Manejo de errores
            self.report({'ERROR'}, f"Error: {str(e)}")  # Muestra error en la UI
            return {'CANCELLED'}  # Indica que la operación falló
        
def register():
    try:
        bpy.utils.register_class(CALCBLENDER_OT_CrearSuperficie)
    except ValueError:
        print("Clase ya registrada, se vuelve a registrar.")
        bpy.utils.unregister_class(CALCBLENDER_OT_CrearSuperficie)
        bpy.utils.register_class(CALCBLENDER_OT_CrearSuperficie)

def unregister():
    try:
        bpy.utils.unregister_class(CALCBLENDER_OT_CrearSuperficie)
    except RuntimeError:
        print("Clase ya estaba desregistrada.")

