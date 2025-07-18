import bpy
import bmesh
import mathutils
from . import logica_gradiente_calculo

class CB_OT_Planotangente(bpy.types.Operator):
    bl_idname = "calcblender.plano_tangente"
    bl_label = "Plano Tangente"
    bl_description = "Crea el plano tangente en el punto (x₀, y₀)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # El operador solo estará disponible si hay un objeto activo con el atributo "funcion"
        obj = context.active_object
        return obj and "funcion" in obj

    def execute(self, context):
        # Acceder a las propiedades personalizadas del addon
        props = context.scene.calcblender_props
        funcion = props.superficie_funcion
        x0, y0 = props.punto_gradiente_x, props.punto_gradiente_y
        
        # Validación de la función 
        if not funcion:
            self.report({'ERROR'}, "Debe ingresar una función z = f(x,y)")
            return {'CANCELLED'}

        # Calcular z0 = f(x0, y0)
        try:
            z0 = eval(funcion, {}, {'x': x0, 'y': y0})
        except Exception as e:
            self.report({'ERROR'}, f"No se pudo evaluar z(x,y): {e}")
            return {'CANCELLED'}

        # Calcular gradiente (df/dx, df/dy) en el punto dado
        grad = logica_gradiente_calculo.calcular_gradiente(funcion, (x0, y0))
        if grad == (0.0, 0.0):
            self.report({'ERROR'}, "Gradiente nulo o inválido")
            return {'CANCELLED'}

        fx, fy = grad

    # Generar plano tangente con fórmula:
        #z = z0 + fx*(x - x0) + fy*(y - y0)
        tamaño = 1  # lado del plano tangente
        offset = [(-tamaño, -tamaño), (tamaño, -tamaño), (tamaño, tamaño), (-tamaño, tamaño)]
        vertices = []
        for dx, dy in offset:
            x = x0 + dx #dx = x- x0
            y = y0 + dy
            z = z0 + fx * dx + fy * dy
            vertices.append((x, y, z))

        # Crear mesh y objeto
        mesh = bpy.data.meshes.new("PlanoTangente")
        bm = bmesh.new()

        verts = [bm.verts.new(co) for co in vertices]
        bm.faces.new(verts)
        bm.to_mesh(mesh)
        bm.free()
        
        # Crear objeto y vincular a la escena
        obj = bpy.data.objects.new("PlanoTangente", mesh)
        context.collection.objects.link(obj)

        # Mostrar la función del plano tangente como mensaje

        context.scene.calcblender_props.plano_tangente_preview = (
            f"z = {z0:.3f} + {fx:.3f}(x - {x0}) + {fy:.3f}(y - {y0})")
        self.report({'INFO'}, f"Plano tangente generado en ({x0}, {y0}, {z0})")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CB_OT_Planotangente)

def unregister():
    bpy.utils.unregister_class(CB_OT_Planotangente)
