bl_info = {
    "name": "Visualizador de Superficies",
    "blender": (3, 0, 0),
    "category": "3D View",
}

import bpy
from . import ui_panel, mesh_surface, gradiente, plano_tangente

def register():
    ui_panel.register()
    mesh_surface.register()
    gradiente.register()
    plano_tangente.register()

def unregister():
    ui_panel.unregister()
    mesh_surface.unregister()
    gradiente.unregister()
    plano_tangente.unregister()
