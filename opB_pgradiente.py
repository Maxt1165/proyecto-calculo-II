import bpy
from . import logica_gradiente_calculo
import bmesh  # type: ignore

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

        grad = logica_gradiente_calculo.calcular_gradiente(funcion, punto)
        if grad == (0.0, 0.0):
            self.report({'ERROR'}, "No se pudo calcular el gradiente o es nulo")
            return {'CANCELLED'}
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 
        escala = 0.5  # puedes ajustar esta escala para que el cono no sea muy largo
        vector = (grad[0] * escala, grad[1] * escala, 0)
        
        # Crear el cono
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.1, depth=0.4)
        cono = context.active_object
        cono.name = f"Gradiente_{punto[0]:.2f}_{punto[1]:.2f}"

        # Ubicar el cono en el punto (x, y, z(x,y))
        obj = context.active_object
        z = 0
        try:
            fz = logica_gradiente_calculo.calcular_gradiente("x*0+y*0+" + funcion, punto)  # quick z = f(x, y) usando expr
            z = eval(funcion, {}, {'x': punto[0], 'y': punto[1]})
        except:
            pass

        cono.location = (punto[0], punto[1], z)

        # Apuntar el cono en la dirección del gradiente
        direccion = mathutils.Vector(vector)
        if direccion.length > 0:
            rotacion = direccion.to_track_quat('Z', 'Y').to_euler()
            cono.rotation_euler = rotacion

        self.report({'INFO'}, f"Gradiente en ({punto[0]}, {punto[1]}) = {grad}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CB_OT_VisualizarGradiente)

def unregister():
    bpy.utils.unregister_class(CB_OT_VisualizarGradiente)
       
"""# Obtener rango de la superficie
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
        return {'FINISHED'} """