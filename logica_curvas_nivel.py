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

def crear_curva_bezier(contorno, nivel_z, nombre_base="CurvaNivel"):
    """Crea curvas Bézier en Blender para una lista de segmentos [(x1, y1), (x2, y2)]
    y los coloca a la altura z = nivel_z.
    Args:
        contorno (list): Lista de segmentos. Cada uno es una lista de dos puntos [(x1, y1), (x2, y2)]
        nivel_z (float): Altura z para las curvas
        nombre_base (str): Nombre base para los objetos creados
    Returns:
        list: Lista de objetos de curva creados"""
    objetos_creados = []

    for idx, segmento in enumerate(contorno):
        if len(segmento) != 2:
            print(f"[Advertencia] Segmento inválido en nivel {nivel_z}: {segmento}")
            continue

        (x1, y1), (x2, y2) = segmento

        # Crear datos de curva
        curva_data = bpy.data.curves.new(name=f"{nombre_base}_data_{idx}", type='CURVE')
        curva_data.dimensions = '3D'
        curva_data.resolution_u = 12
        curva_data.bevel_depth = 0.02
        curva_data.bevel_resolution = 3

        # Crear spline con 2 puntos Bézier
        spline = curva_data.splines.new(type='BEZIER')
        spline.bezier_points.add(1)

        puntos = [(x1, y1), (x2, y2)]
        for i, (x, y) in enumerate(puntos):
            p = spline.bezier_points[i]
            p.co = (x, y, nivel_z)
            p.handle_left_type = 'AUTO'
            p.handle_right_type = 'AUTO'

        # Nombre único por segmento
        nombre_obj = f"{nombre_base}_z{nivel_z:.2f}_s{idx}"
        if nombre_obj in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nombre_obj], do_unlink=True)

        curva_obj = bpy.data.objects.new(nombre_obj, curva_data)
        bpy.context.collection.objects.link(curva_obj)
        #Esto asegura que cada objeto tenga el material antes de ser retornado.
        curva_obj.data.materials.append(bpy.data.materials.get("CurvasMaterial") or bpy.data.materials.new("CurvasMaterial"))
        objetos_creados.append(curva_obj)
        
    return objetos_creados
