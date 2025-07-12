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


#def register():
   # ui_panel.register()

#def unregister():
   # ui_panel.unregister()

# ESTO ACTUALIZARA LOS MODULOS (ARCHIVOS) CADA QUE SE RECARGA ESTE __init__.py
import importlib
from . import ui_panel
_modules = [ui_panel]

def _reload_modules():
    for m in _modules:
        importlib.reload(m)

def register():
    _reload_modules()
    
    # Registrar módulos base (como ui_panel)
    for m in _modules:
        if hasattr(m, "register"):
            m.register()

    # Importar componentes después del arranque (evita ciclos)
    from visualizador_superficies.operacionesBlender import (
        superficie_opB,
        gradiente_opB,
        ptangente_opB,
    )



    # 1. Propiedades


    # 2. Operadores
    #operacionesBlender.superficie_opB.register()
    #operacionesBlender.gradiente_opB.register()
    ptangente_opB.register()

    # 3. Panel UI
    ui_panel.register()

    # 4. Inicializar adaptador o servicios



def unregister():
    from visualizador_superficies.operacionesBlender import (
        superficie_opB,
        gradiente_opB,
        ptangente_opB,
    )


    # Desregistrar en orden inverso
    ui_panel.unregister()
    #operacionesBlender.ptangente_opB.unregister()
    #operacionesBlender.gradiente_opB.unregister()
    superficie_opB.unregister()
    

    # Si hay que cerrar algo del adaptador, sería aquí

    # Finalmente, desregistrar ui_panel y otros módulos
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            m.unregister()

