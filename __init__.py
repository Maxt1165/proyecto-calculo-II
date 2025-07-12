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

#def register():
   # ui_panel.register()

#def unregister():
   # ui_panel.unregister()

# ESTO ACTUALIZARA LOS MODULOS (ARCHIVOS) CADA QUE SE RECARGA ESTE __init__.py
import importlib
print("Se importó importlib en el archivo __init__.py")
from . import ui_panel
print("Se importó ui_panel en el archivo __init__.py")
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
    from . import opB_superficie
    print("Se importó opB_superficie en el archivo __init__.py")


    # 1. Propiedades


    # 2. Operadores
    #operacionesBlender.superficie_opB.register()
    #operacionesBlender.gradiente_opB.register()
    opB_superficie.register()

    # 3. Panel UI
    #ui_panel.register()

    # 4. Inicializar adaptador o servicios



def unregister():
    from . import opB_superficie
    print("Se importó opB_superficie en el archivo __init__.py")
    # Desregistrar en orden inverso
    #ui_panel.unregister()
    #operacionesBlender.ptangente_opB.unregister()
    #operacionesBlender.gradiente_opB.unregister()
    opB_superficie.unregister()
    

    # Si hay que cerrar algo del adaptador, sería aquí

    # Finalmente, desregistrar ui_panel y otros módulos
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            m.unregister()

