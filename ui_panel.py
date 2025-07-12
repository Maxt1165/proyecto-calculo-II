import bpy

class VISUALIZADOR_PT_Panel(bpy.types.Panel):
    bl_label = "Panel de Prueba"
    bl_idname = "VISUALIZADOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Superficies'

    def draw(self, context):
        layout = self.layout
        layout.label(text="GANARON LsdfghjOS MALOS 🗣️")

def register():
    bpy.utils.register_class(VISUALIZADOR_PT_Panel)

def unregister():
    bpy.utils.unregister_class(VISUALIZADOR_PT_Panel)
