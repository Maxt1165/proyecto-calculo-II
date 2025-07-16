import numpy as np
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

    if not niveles:
        raise ValueError("La lista de niveles de curvas está vacía.")

    resultado = {nivel: [] for nivel in niveles}

    for i in range(resolucion - 1):
        for j in range(resolucion - 1):
            # Puntos del cuadro
            puntos = [
                (x[j],     y[i],     Z[i][j]),     # A
                (x[j+1],   y[i],     Z[i][j+1]),   # B
                (x[j+1],   y[i+1],   Z[i+1][j+1]), # C
                (x[j],     y[i+1],   Z[i+1][j])    # D
            ]
    
            for nivel in niveles:
                # Interpolar sobre los bordes si el nivel cruza entre dos valores
                edges = []
                for k, (p1, p2) in enumerate(zip(puntos, puntos[1:] + [puntos[0]])):
                    z1, z2 = p1[2], p2[2]
                    if (z1 - nivel) * (z2 - nivel) < 0:  # Cruce
                        t = (nivel - z1) / (z2 - z1)
                        x_interp = p1[0] + t * (p2[0] - p1[0])
                        y_interp = p1[1] + t * (p2[1] - p1[1])
                        edges.append((x_interp, y_interp))
                if len(edges) == 2:
                    resultado[nivel].append(edges)  # Línea entre dos puntos
    return resultado
def conectar_segmentos(segmentos, tolerancia=1e-5):
    """
    Une segmentos [(x1,y1),(x2,y2)] en trayectorias continuas [(x0,y0),(x1,y1),...].
    Args:
        segmentos (list): Lista de segmentos, cada uno = [(x1,y1), (x2,y2)]
        tolerancia (float): Distancia mínima para considerar puntos conectados.
    Returns:
        list: Lista de curvas, cada curva es una lista de puntos [(x, y), ...]
    """
    import math
    def son_cercanos(p1, p2):
        return math.hypot(p1[0]-p2[0], p1[1]-p2[1]) < tolerancia

    pendientes = segmentos.copy()
    curvas = []

    while pendientes:
        seg = pendientes.pop()
        curva = [seg[0], seg[1]]

        conectado = True
        while conectado:
            conectado = False
            for i, s in enumerate(pendientes):
                if son_cercanos(curva[-1], s[0]):
                    curva.append(s[1])
                    pendientes.pop(i)
                    conectado = True
                    break
                elif son_cercanos(curva[-1], s[1]):
                    curva.append(s[0])
                    pendientes.pop(i)
                    conectado = True
                    break
                elif son_cercanos(curva[0], s[1]):
                    curva.insert(0, s[0])
                    pendientes.pop(i)
                    conectado = True
                    break
                elif son_cercanos(curva[0], s[0]):
                    curva.insert(0, s[1])
                    pendientes.pop(i)
                    conectado = True
                    break
        curvas.append(curva)
    return curvas

def crear_curva_bezier(segmentos, nivel_z, nombre_base="CurvaNivel"):
    """Crea curvas Bézier en Blender desde segmentos [(x1,y1),(x2,y2)], conectándolos en trayectorias continuas."""
    objetos_creados = []  # Lista donde se guardarán los objetos creados
    
    # Conectamos los segmentos individuales en trayectorias más largas y suaves
    curvas_conectadas = conectar_segmentos(segmentos)

    # Iteramos sobre cada trayectoria conectada
    for idx, puntos in enumerate(curvas_conectadas):
        if len(puntos) < 2:
            continue  # No se puede construir una curva con menos de 2 puntos

        # Si ya existe un objeto de curva con el mismo nombre, eliminarlo
        nombre_data = f"{nombre_base}_data_{idx}"
        if nombre_data in bpy.data.curves:
            bpy.data.curves.remove(bpy.data.curves[nombre_data], do_unlink=True)

        # Crear un nuevo objeto de tipo CURVE
        curva_data = bpy.data.curves.new(name=nombre_data, type='CURVE')
        curva_data.dimensions = '3D'               # Permite colocar puntos en 3D
        curva_data.resolution_u = 12               # Suavidad de la curva
        curva_data.bevel_depth = 0.02              # Grosor visual del trazo
        curva_data.bevel_resolution = 3            # Resolución del bisel

        # Añadir un spline Bézier a la curva
        spline = curva_data.splines.new(type='BEZIER')
        spline.bezier_points.add(len(puntos) - 1)  # Ya existe 1 por defecto

        # Establecer los puntos de control del spline
        for i, (x, y) in enumerate(puntos):
            p = spline.bezier_points[i]
            p.co = (x, y, nivel_z)              # Coordenada del punto en 3D
            p.handle_left_type = 'AUTO'         # Los manejadores se ajustan automáticamente
            p.handle_right_type = 'AUTO'

        # Si el primer y último punto están muy cerca, cerrar la curva
        if (mathutils.Vector(puntos[0]) - mathutils.Vector(puntos[-1])).length < 1e-2:
            spline.use_cyclic_u = True

        # Crear nombre único para el objeto Blender
        nombre_obj = f"{nombre_base}_z{nivel_z:.2f}_c{idx}"
        if nombre_obj in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nombre_obj], do_unlink=True)

        # Crear objeto Blender y vincularlo a la escena
        curva_obj = bpy.data.objects.new(nombre_obj, curva_data)
        bpy.context.scene.collection.objects.link(curva_obj)

        # Asignar material personalizado (crearlo si no existe)
        if "CurvasMaterial" not in bpy.data.materials:
            mat = bpy.data.materials.new(name="CurvasMaterial")
        else:
            mat = bpy.data.materials["CurvasMaterial"]
        curva_obj.data.materials.append(mat)

        # Añadir el objeto a la lista final
        objetos_creados.append(curva_obj)

    # Devolver la lista de objetos creados
    return objetos_creados

