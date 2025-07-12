import bpy
from . import logica_gradiente_calculo
import bmesh  # type: ignore

class CB_OT_VisualizarGradiente(bpy.types.Operator):
    bl_idname = "calcblender.visualizar_gradiente"
    bl_label = "Visualizar Gradiente"
    bl_description = "Crea una representación visual del campo vectorial gradiente"
    bl_options = {'REGISTER', 'UNDO'}
    
    resolucion = bpy.props.IntProperty(
        name="Resolución",
        default=10,
        min=3,
        max=30
    )

    @classmethod
    def poll(cls, context):
        # Solo disponible si hay una superficie seleccionada
        obj = context.active_object
        return obj and "funcion" in obj
    
    def execute(self, context):
        obj = context.active_object
        funcion = obj["funcion"]
        
        # Obtener rango de la superficie
        x_min = min(v.co.x for v in obj.data.vertices)
        x_max = max(v.co.x for v in obj.data.vertices)
        y_min = min(v.co.y for v in obj.data.vertices)
        y_max = max(v.co.y for v in obj.data.vertices)
        
        # Calcular vectores gradientes
        vectores = logica_gradiente_calculo.vector_gradiente(
            funcion,
            (x_min, x_max),
            (y_min, y_max),
            self.resolucion
        )
        
        # Crear curva vacía para almacenar vectores
        nombre = f"Gradiente_{funcion}"
        curva = bpy.data.curves.new(nombre, 'CURVE')
        curva.dimensions = '3D'
        
        # Crear flechas para cada vector
        for origen, vector in vectores:
                mesh_flecha = bpy.data.meshes.new("Flecha")
                bm = bmesh.new()

                destino = (
                    origen[0] + vector[0],
                    origen[1] + vector[1],
                    origen[2] + vector[2]
                )

                v1 = bm.verts.new(origen)
                v2 = bm.verts.new(destino)
                bm.edges.new((v1, v2))

                bm.to_mesh(mesh_flecha)
                bm.free()

                obj_flecha = bpy.data.objects.new("Flecha", mesh_flecha)
                context.collection.objects.link(obj_flecha)
        self.report({'INFO'}, f"Campo gradiente creado para {funcion}")
        return {'FINISHED'}