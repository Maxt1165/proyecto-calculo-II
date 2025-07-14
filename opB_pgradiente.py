import bpy
from . import logica_gradiente_calculo
import bmesh  # type: ignore
import mathutils # type: ignore

class CB_OT_VisualizarGradiente(bpy.types.Operator):
    bl_idname = "calcblender.visualizar_gradiente"
    bl_label = "Visualizar Gradiente"
    bl_description = "Calcula y visualiza el gradiente en un punto dado (x,y)"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Solo disponible si hay una superficie seleccionada
        obj = context.active_object
        return obj and "funcion" in obj
    
    def execute(self, context):
        props = context.scene.calcblender_props
        funcion = props.superficie_funcion
        punto = (props.punto_gradiente_x, props.punto_gradiente_y)

        # Validación de la función
        if not funcion:
            self.report({'ERROR'}, "Debes ingresar una función z = f(x, y)")
            return {'CANCELLED'}
        grad = logica_gradiente_calculo.calcular_gradiente(funcion, punto)
        # Manejo de errores por si el gradiente es 0
        if grad == (0.0, 0.0):
            self.report({'ERROR'}, "No se pudo calcular el gradiente o es nulo")
            return {'CANCELLED'}
        # Calcular z = f(x, y)
        try:
            z = eval(funcion, {}, {'x': punto[0], 'y': punto[1]})
        except Exception as e:
            self.report({'ERROR'}, f"No se pudo evaluar z en el punto: {e}")
            return {'CANCELLED'}
        
        # Crear el cono como vector gradiente  normal
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.3, depth=1.6) 
        cono = context.active_object
        cono.name = f"Gradiente_{punto[0]:.2f}_{punto[1]:.2f}"
        cono.location=(punto[0], punto[1], z) #posicionamiento en la superficie

        # Construimos el vector normal: (∂f/∂x, ∂f/∂y, -1)
        direccion = mathutils.Vector((grad[0], grad[1], -1))
        if direccion.length > 0:
            direccion.normalize()
            rotacion = direccion.to_track_quat('Z', 'Y').to_euler()
            cono.rotation_euler = rotacion
        # Mostrar el resultado en pantalla
        self.report({'INFO'}, f"Gradiente en ({punto[0]}, {punto[1]}) = {grad}")
        props.gradiente_preview = f"∇f({punto[0]:.2f}, {punto[1]:.2f}) = ({grad[0]:.3f}, {grad[1]:.3f})"
        return {'FINISHED'} 
    

def register():
    bpy.utils.register_class(CB_OT_VisualizarGradiente)

def unregister():
    bpy.utils.unregister_class(CB_OT_VisualizarGradiente)