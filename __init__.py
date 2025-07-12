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
print("Se importó bpy en el archivo __init__.py")

# ESTO ACTUALIZARÁ LOS MÓDULOS (ARCHIVOS) CADA QUE SE RECARGUE ESTE __init__.py
import importlib
from . import ui_panel
from . import util_propiedades

from . import logica_superficie_generar
from . import logica_soporte_matematica
from . import opB_superficie

from . import logica_gradiente_calculo
from . import opB_pgradiente

from . import opB_ptangente

_modules = [ui_panel, util_propiedades, 
            logica_superficie_generar, logica_soporte_matematica, opB_superficie,
            logica_gradiente_calculo, opB_pgradiente,
            opB_ptangente]  # AQUI SE AÑADIRAN LOS MODULOS A DESARROLLAR

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
