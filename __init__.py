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
from . import util_propiedades

from . import logica_superficie_generar
from . import logica_soporte_matematica
from . import opB_superficie

from . import logica_gradiente_calculo
from . import opB_pgradiente
from . import opB_ptangente

from . import logica_curvas_nivel
from . import opB_curvas_nivel

from . import logica_integral_calculo
from . import opB_integral

from . import ui_panel

_modules = [ util_propiedades, 
            logica_superficie_generar, logica_soporte_matematica, opB_superficie,
            logica_gradiente_calculo, opB_pgradiente, opB_ptangente, 
            logica_curvas_nivel, opB_curvas_nivel,
            logica_integral_calculo, opB_integral,
            ui_panel]  # AQUI SE AÑADEN LOS MODULOS A DESARROLLAR

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
