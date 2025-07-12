import numpy as np
print('Se importó numpy en el archivo superficie_generar')
import bpy
print('Se importó bpy en el archivo superficie_generar')
import bmesh # type: ignore
print('Se importó bmesh en el archivo superficie_generar')
from .logica_soporte_matematica import hacerfuncion_segura
print('Se importó safe_lambdify de .soporte_matematica')

"""Propósito:Generar una superficie 3D en Blender a partir de una
expresión matemática z=f(x,y), usando NumPy, SymPy y BMesh (eficiencia)"""
#CUADRICULA = GRID

def crear_superficie(expresion, x_dominio, y_dominio, resolucion):
    # 1. Preparar función vectorizada
    """Convierte la expresión simbólica expresion en una función NumPy-evaluable"""
    f = hacerfuncion_segura(expresion)
    
    # 2. Crear grid 2D de puntos para las variables optimizado con NumPy
    x = np.linspace(*x_dominio, resolucion)
    y = np.linspace(*y_dominio, resolucion)
    X, Y = np.meshgrid(x, y) #genera las coordenadas en forma matricial
    Z = f(X, Y)
    
    # 3. Crear malla con BMesh
    """Sistema de edición de mallas eficiente en Blender (ideal para geometrías dinámicas)
    Aquí se va a crear la geometría punto por punto y luego se armarán las caras"""
    bm = bmesh.new()
    verts = bm.verts
    
    # Agregar vértices  en cada punto del grid 3D
    for j in range(resolucion):
        for i in range(resolucion):
            verts.new((X[i,j], Y[i,j], Z[i,j]))
    
    # Crear caras: Une los vértices adyacentes para formar caras cuadradas/quads
    for j in range(resolucion-1):
        for i in range(resolucion-1):
            idx = j * resolucion + i
            bm.faces.new((
                verts[idx], 
                verts[idx+1], 
                verts[idx+resolucion+1], 
                verts[idx+resolucion]
            ))
    
    # 4. Crear objeto que aparezca: Se crea un nuevo objeto malla/mesh
        # y se transfiere la geometría generada.
    malla = bpy.data.meshes.new(name=f"Superficie_{expresion}")
    bm.to_mesh(malla)
    bm.free() #libera la memoria usada por BMesh
    
    #Se añade el objeto creado al contexto actual de Blender (la escena activa).
    obj = bpy.data.objects.new(malla.name, malla)
    bpy.context.collection.objects.link(obj)
    
    # 5. Optimizar para viewport
    malla.update() #asegura que la geometría esté lista para el renderizado.
    malla.calc_normals() #mejora la iluminación y sombreado de la superficie.
    
    return obj