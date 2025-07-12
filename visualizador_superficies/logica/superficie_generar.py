import numpy as np
import bpy
import bmesh
from .soporte_matematica import safe_lambdify

def create_surface(expression, x_domain, y_domain, resolution):
    """Crea una superficie 3D a partir de z=f(x,y) en Blender 4.4.3"""
    # 1. Preparar función vectorizada
    f = safe_lambdify(expression)
    
    # 2. Crear grid optimizado con NumPy
    x = np.linspace(*x_domain, resolution)
    y = np.linspace(*y_domain, resolution)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    
    # 3. Crear malla con BMesh (más eficiente en Blender 4.4.3)
    bm = bmesh.new()
    verts = bm.verts
    
    # Agregar vértices
    for j in range(resolution):
        for i in range(resolution):
            verts.new((X[i,j], Y[i,j], Z[i,j]))
    
    # Crear caras
    for j in range(resolution-1):
        for i in range(resolution-1):
            idx = j * resolution + i
            bm.faces.new((
                verts[idx], 
                verts[idx+1], 
                verts[idx+resolution+1], 
                verts[idx+resolution]
            ))
    
    # 4. Crear objeto en escena
    mesh = bpy.data.meshes.new(name=f"Superficie_{expression}")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # 5. Optimizar para viewport
    mesh.update()
    mesh.calc_normals()
    
    return obj