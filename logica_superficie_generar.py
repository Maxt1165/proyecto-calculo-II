import numpy as np
import bpy
import bmesh # type: ignore
from .logica_soporte_matematica import hacerfuncion_segura

print('Se importaron los módulos necesarios')

"""Propósito:Generar una superficie 3D en Blender a partir de una
expresión matemática z=f(x,y), usando NumPy, SymPy y BMesh (eficiencia)"""
#CUADRICULA = GRID

def crear_superficie(expresion, x_dominio, y_dominio, resolucion,props):
    # 1. Preparar función vectorizada(numpy_evaluable)
    """Convierte la expresión simbólica expresion en una función NumPy-evaluable"""
    f = hacerfuncion_segura(expresion)
    
    # 2. Crear grid 2D de coordenadas/optimizado con NumPy
    x = np.linspace(*x_dominio, resolucion)
    y = np.linspace(*y_dominio, resolucion)
    X, Y = np.meshgrid(x, y) #genera las coordenadas en forma matricial
    Z = f(X, Y)
# Limitar altura visual entre Z min y Z max desde UI
    Z = np.clip(Z, props.superficie_z_min, props.superficie_z_max)

    # 3. Crear malla con BMesh
    """Sistema de edición de mallas eficiente en Blender (ideal para geometrías dinámicas)
    Aquí se va a crear la geometría punto por punto y luego se armarán las caras"""
    bm = bmesh.new()
    verts = []
    
    # Crear vértices  en cada punto del grid 3D
    for j in range(resolucion):
        for i in range(resolucion):
            coord=(X[i,j], Y[i,j], Z[i,j])
            verts.append(bm.verts.new(coord))
   
    bm.verts.ensure_lookup_table() #EVITAR ERROR:Este error ocurre cuando se accede 
                                #a los vértices de un objeto BMesh (como bm.verts[index]) sin haber actualizado la tabla interna de índices.

    # Crear caras: Une los vértices adyacentes para formar caras cuadradas/quads
    for j in range(resolucion-1):
        for i in range(resolucion-1):
            idx = j * resolucion + i
            try:
                bm.faces.new((
                    verts[idx], 
                    verts[idx+1], 
                    verts[idx+resolucion+1], 
                    verts[idx+resolucion]
                ))
            except ValueError:
                pass  # cara ya creada se omite

    # 4. Crear objeto: Se crea un nuevo objeto malla/mesh
        # y se transfiere la geometría generada.
    malla = bpy.data.meshes.new(name=f"Superficie_{expresion}")
    bm.to_mesh(malla)
    bm.free() #libera la memoria usada por BMesh
    
    #Se añade el objeto creado al contexto actual de Blender (la escena activa).
    obj = bpy.data.objects.new(malla.name, malla)
    bpy.context.collection.objects.link(obj)
    
    # 5. Optimizar para viewport
    malla.update()
    
    return obj