bl_info = {
    "name":        "Visualizador de Superficies y Gradientes",
    "description": "Genera superficies z=f(x,y), curvas de nivel, gradiente y plano tangente",
    "author":      "Equipo Cálculo II (2025‑I)",
    "version":     (0, 1, 0),
    "blender":     (3, 0, 0),          # Versión mínima de Blender
    "location":    "View3D › Sidebar › Superficies",
    "category":    "3D View",
}

# ------------------------------------------------------------------ #
#  IMPORTACIÓN DE SUBMÓDULOS
# ------------------------------------------------------------------ #
import importlib
from . import ui_panel, mesh_surface, gradiente, plano_tangente

#  Poner los módulos en una lista facilita registrar / anular registro
_modules = [ui_panel, mesh_surface, gradiente, plano_tangente]


def _reload_submodules():
    """Recarga en caliente cada submódulo (útil durante el desarrollo)."""
    for m in _modules:
        importlib.reload(m)


# ------------------------------------------------------------------ #
#  FUNCIONES DE REGISTRO OBLIGATORIAS PARA TODO ADD‑ON
# ------------------------------------------------------------------ #
def register():
    _reload_submodules()        # Recarga si el add‑on ya estaba activo
    for m in _modules:          # Llama register() de cada archivo
        if hasattr(m, "register"):
            m.register()


def unregister():
    for m in reversed(_modules):  # En orden inverso por seguridad
        if hasattr(m, "unregister"):
            m.unregister()
