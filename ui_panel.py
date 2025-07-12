import bpy
from . import gui

class VISUALIZADOR_PT_Panel(bpy.types.Panel):
    bl_label = "Panel de Prueba"
    bl_idname = "VISUALIZADOR_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Superficies'

    def draw(self, context):
        layout = self.layout
        layout.label(text="GANARON LOS MALOS 🗣️")


#Registro del panel CALCBLENDER_PT_SurfacePanel
def register():
    # Registra tu panel principal de superficies
    bpy.utils.register_class(gui.CALCBLENDER_PT_SurfacePanel)
    
    # Registra este panel adicional si lo necesitas
    bpy.utils.register_class(VISUALIZADOR_PT_Panel)

def unregister():
    # Desregistra en orden inverso
    bpy.utils.unregister_class(VISUALIZADOR_PT_Panel)
    bpy.utils.unregister_class(gui.CALCBLENDER_PT_SurfacePanel)