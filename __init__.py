bl_info = {
    "name":        "visualizador_superficies",
    "description": "Genera superficies z=f(x,y), curvas de nivel, gradiente y plano tangente",
    "author":      "LyM",
    "version":     (0, 1, 0),
    "blender":     (4, 4, 3),
    "location":    "View3D › Sidebar › Superficies",
    "category":    "3D View",
}

import bpy
from . import ui_panel

def register():
    ui_panel.register()

def unregister():
    ui_panel.unregister()
    
# ESTO ACTUALIZARA LOS MODULOS (ARCHIVOS) CADA QUE SE RECARGA ESTE __init__.py

import importlib

from . import ui_panel, mesh_surface, gradiente, plano_tangente

_modules = [ui_panel, mesh_surface, gradiente, plano_tangente]

def _reload_modules():
    for m in _modules:
        importlib.reload(m)

def register():
    _reload_modules()
    for m in _modules:
        if hasattr(m, "register"):
            m.register()

def unregister():
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            m.unregister()

