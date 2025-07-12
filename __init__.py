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
from  .import gui
from .import operacionesBlender
from .import utilidades

def register():
    ui_panel.register()

def unregister():
    ui_panel.unregister()

# ESTO ACTUALIZARA LOS MODULOS (ARCHIVOS) CADA QUE SE RECARGA ESTE __init__.py
import importlib
from . import ui_panel
_modules = [ui_panel]

def _reload_modules():
    for m in _modules:
        importlib.reload(m)

def register():
    _reload_modules()
    for m in _modules:
        if hasattr(m, "register"):
            m.register()



    # Registrar propiedades primero
    gui.propiedades.register() 
    
    # Registrar operadores
    operacionesBlender.superficie_opB.register()
    operacionesBlender.gradiente_opB.register()
    operacionesBlender.ptangente_opB.register()
    
    # Registrar UI
    gui.main_panel.register()
    
    # Configurar adaptador
    utilidades.AdaptorApiB.init()

def unregister():
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            m.unregister()
    
    gui.main_panel.unregister()
    operacionesBlender.ptangente_opB.unregister()
    operacionesBlender.gradiente_opB.unregister()
    operacionesBlender.superficie_opB.unregister()
    gui.propiedades.unregister()

