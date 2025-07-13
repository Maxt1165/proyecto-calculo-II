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
    #REGISTER: Hace visible el operador en la UI /permite asignar atajos de teclado.
    #Permite deshacer la acción con Ctrl+Z.
    bl_idname = "visualizador_superficies.crearsuperficie"
    bl_label = "Crear Superficie"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    #Verifica si el operador puede ejecutarse 
    def poll(cls, contexto):
        return contexto.mode == 'OBJECT'

    #METODO EJECUTABLE CUANDO EL USUARIO DA CLIC EN CREAR SUPERFICIE
    """carga las propiedades guardadas (función matemática y rangos)
    desde Blender para usarlas en cálculos"""
    def execute(self, context):
        props = context.scene.calcblender_props  # Accede directamente a las propiedades del operador

        if not props.superficie_funcion.strip():
            self.report({'ERROR'}, "Debes ingresar una función z = f(x, y)")
            return {'CANCELLED'}
    
        try:
            obj = logica_superficie_generar.crear_superficie(
                expresion=props.superficie_funcion,
                x_dominio=(props.superficie_x_min, props.superficie_x_max),
                y_dominio=(props.superficie_y_min, props.superficie_y_max),
                resolucion=props.superficie_resolucion,
                props=props  # configurar rango visual z
            )
            obj.location = context.scene.cursor.location
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = obj
            obj.select_set(True)
            obj.modifiers.new(name="Suavizado", type='SMOOTH')
            obj["funcion"] = props.superficie_funcion  # importante para el gradiente
            self.report({'INFO'}, f"Superficie creada: {obj.name}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}
        
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