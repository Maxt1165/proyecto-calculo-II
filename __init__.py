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


# ------------------------------------------------------------------ #
#  IMPORTACIÓN DE SUBMÓDULOS
# ------------------------------------------------------------------ #
import importlib
from . import ui_panel, mesh_surface

_modules = [ui_panel, mesh_surface]

def _reload_modules():
    for m in _modules:
        importlib.reload(m)


# ------------------------------------------------------------------ #
#  FUNCIONES DE REGISTRO OBLIGATORIAS PARA TODO ADD‑ON
# ------------------------------------------------------------------ #
#def register():
#    _reload_submodules()        # Recarga si el add‑on ya estaba activo
#    for m in _modules:          # Llama register() de cada archivo
#        if hasattr(m, "register"):
#            m.register()


#def unregister():
 #   for m in reversed(_modules):  # En orden inverso por seguridad
  #      if hasattr(m, "unregister"):
   #         m.unregister()
