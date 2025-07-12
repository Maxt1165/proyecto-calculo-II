import bpy

class VISUALIZADOR_PT_MainPanel(bpy.types.Panel):
    bl_label = "Visualizador de Superficies"
    bl_idname = "VISUALIZADOR_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Superficies'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Panel listo para comenzar")

def register():
    bpy.utils.register_class(VISUALIZADOR_PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(VISUALIZADOR_PT_MainPanel)
