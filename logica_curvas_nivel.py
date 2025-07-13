import numpy as np
import matplotlib.pyplot as plt
from .logica_soporte_matematica import hacerfuncion_segura
import bpy
import mathutils

def obtener_curvas_de_nivel(expr, x_range, y_range, resolucion, niveles):
    """ Evalúa la función z = f(x, y) y devuelve las curvas de nivel como listas de puntos (por nivel).
    Args:
        expr (str): Expresión matemática (por ejemplo, "x**2 + y**2")
        x_range (tuple): Dominio en x (xmin, xmax)
        y_range (tuple): Dominio en y (ymin, ymax)
        resolucion (int): Número de puntos por eje
        niveles (list): Lista de niveles z para generar las curvas
    Returns:
        dict: Diccionario donde clave = nivel, valor = lista de curvas (cada curva = lista de (x, y))"""
    # Paso 1: Crear función evaluable segura
    f = hacerfuncion_segura(expr)
    
    # Paso 2: Crear grilla de puntos (malla regular)
    x = np.linspace(*x_range, resolucion)
    y = np.linspace(*y_range, resolucion)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    # Paso 3: Usar matplotlib para obtener contornos
    fig, ax = plt.subplots()
    contornos = ax.contour(X, Y, Z, levels=niveles)
    
    resultado = {}
    for nivel, coleccion in zip(contornos.levels, contornos.collections):
        curvas = []
        for path in coleccion.get_paths():
            v = path.vertices  # Lista de (x, y)
            if len(v) >= 2:
                curvas.append(v.tolist())
        resultado[nivel] = curvas
    
    plt.close(fig)  # Cierra la figura para evitar consumir memoria
    return resultado

#Para cada curva obtenida desde matplotlib.contour, crearemos una curva de Bézier en Blender a la altura z = nivel
def crear_curva_bezier(contorno, nivel_z, nombre="CurvaNivel"):
    """Crea una curva Bézier en Blender desde una lista de puntos [(x, y), ...],
    y la coloca en z = nivel_z."""
    if len(contorno) < 2:
        return None

    # 1. Crear un nuevo objeto de tipo CURVE
    curva_data = bpy.data.curves.new(name=nombre, type='CURVE')
    curva_data.dimensions = '3D'
    curva_data.resolution_u = 12  # Suavidad
    
    # Mejora de visibilidad en viewport
    curva_data.bevel_depth = 0.02
    curva_data.bevel_resolution = 3


    # 2. Crear un spline Bézier
    spline = curva_data.splines.new(type='BEZIER')
    spline.bezier_points.add(len(contorno) - 1)  # Ya hay 1 por defecto

    for i, (x, y) in enumerate(contorno):
        punto = spline.bezier_points[i]
        punto.co = (x, y, nivel_z)  # Punto de control central
        punto.handle_left_type = 'AUTO'
        punto.handle_right_type = 'AUTO'

    # 3. Opcional: cerrar la curva si el primer y último punto son cercanos
    if (mathutils.Vector(contorno[0]) - mathutils.Vector(contorno[-1])).length < 1e-2:
        spline.use_cyclic_u = True

    # 4. Crear el objeto en la escena
    nombre_objeto = f"{nombre}_z{nivel_z:.1f}"
    
    # Eliminar objeto previo con mismo nombre (si existe)
    if nombre_objeto in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[nombre_objeto], do_unlink=True)
    curva_obj = bpy.data.objects.new(nombre_objeto, curva_data)
    bpy.context.collection.objects.link(curva_obj)
    
    return curva_obj

def animar_curvas_a_plano(objetos_curvas, frame_inicio=1, duracion=20):
    """ Anima curvas desde su altura actual (z = nivel) hasta z = 0. 
    Args:
        objetos_curvas (list): Lista de objetos de tipo curva (bpy.types.Object)
        frame_inicio (int): Cuadro inicial de la animación
        duracion (int): Número de cuadros que durará la caída"""
    
    for i, curva_obj in enumerate(objetos_curvas):
        if not curva_obj or curva_obj.type != 'CURVE':
            continue  # ignorar objetos inválidos
        
        # Frame base para esta curva (puedes escalonar si quieres)
        f_ini = frame_inicio + i
        f_fin = f_ini + duracion

        # Posición original
        z_original = curva_obj.location.z

        # Keyframe en altura original
        curva_obj.location.z = z_original
        curva_obj.keyframe_insert(data_path="location", frame=f_ini)

        # Keyframe en z = 0
        curva_obj.location.z = 0.0
        curva_obj.keyframe_insert(data_path="location", frame=f_fin)

