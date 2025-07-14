import sympy as sp
import numpy as np
import bmesh
import bpy
from .logica_soporte_matematica import hacerfuncion_segura

def calcular_integral_definida(expr_str, a, b, c, d):
    """
    Calcula la integral doble definida de una función z = f(x,y) sobre [a,b] x [c,d]
    """
    x, y = sp.symbols('x y')
    try:
        f = sp.sympify(expr_str)
        integral = sp.integrate(f, (x, a, b), (y, c, d))
        return float(integral)
    except Exception as e:
        print(f"[ERROR] No se pudo calcular la integral: {e}")
        return None
    
def crear_prisma_integral(expr, x_dominio, y_dominio, resolucion_sup, resolucion_lados=6):
    f = hacerfuncion_segura(expr)

    # Malla superior
    x = np.linspace(*x_dominio, resolucion_sup)
    y = np.linspace(*y_dominio, resolucion_sup)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    bm = bmesh.new() # Aquí crea la malla
    verts_sup = [] # Arreglo para los vértices de la superficie
    verts_base = [] # Arreglo para los vértices de la base

    for j in range(resolucion_sup):
        for i in range(resolucion_sup):
            v_top = bm.verts.new((X[i, j], Y[i, j], Z[i, j]))
            v_bot = bm.verts.new((X[i, j], Y[i, j], 0))
            verts_sup.append(v_top)
            verts_base.append(v_bot)

    bm.verts.ensure_lookup_table()

    # Caras superiores e inferiores
    for j in range(resolucion_sup - 1):
        for i in range(resolucion_sup - 1):
            idx = j * resolucion_sup + i
            try:
                bm.faces.new((
                    verts_sup[idx],
                    verts_sup[idx + 1],
                    verts_sup[idx + resolucion_sup + 1],
                    verts_sup[idx + resolucion_sup]
                ))
                bm.faces.new((
                    verts_base[idx + resolucion_sup],
                    verts_base[idx + resolucion_sup + 1],
                    verts_base[idx + 1],
                    verts_base[idx]
                ))
            except:
                continue

    # FUNCIONES PARA LATERALES
    def cara_lateral(p1, p2, p3, p4):
        try:
            bm.faces.new((p1, p2, p3, p4))
        except:
            pass

    def generar_laterales_eje_x(y_val):
        xs = np.linspace(*x_dominio, resolucion_lados)
        z_vals = f(xs, y_val)
        for i in range(resolucion_lados - 1):
            x1, x2 = xs[i], xs[i + 1]
            z1, z2 = z_vals[i], z_vals[i + 1]

            v1 = bm.verts.new((x1, y_val, 0))
            v2 = bm.verts.new((x2, y_val, 0))
            v3 = bm.verts.new((x2, y_val, z2))
            v4 = bm.verts.new((x1, y_val, z1))
            cara_lateral(v1, v2, v3, v4)

    def generar_laterales_eje_y(x_val):
        ys = np.linspace(*y_dominio, resolucion_lados)
        z_vals = f(x_val, ys)
        for i in range(resolucion_lados - 1):
            y1, y2 = ys[i], ys[i + 1]
            z1, z2 = z_vals[i], z_vals[i + 1]

            v1 = bm.verts.new((x_val, y1, 0))
            v2 = bm.verts.new((x_val, y2, 0))
            v3 = bm.verts.new((x_val, y2, z2))
            v4 = bm.verts.new((x_val, y1, z1))
            cara_lateral(v1, v2, v3, v4)

    # Generar los 4 laterales del prisma
    generar_laterales_eje_x(y_dominio[0])  # lado y = y_min
    generar_laterales_eje_x(y_dominio[1])  # lado y = y_max
    generar_laterales_eje_y(x_dominio[0])  # lado x = x_min
    generar_laterales_eje_y(x_dominio[1])  # lado x = x_max

    # Asigna el objeto creado a la malla
    mesh = bpy.data.meshes.new("Prisma_Integral")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("Prisma_Integral", mesh)
    bpy.context.collection.objects.link(obj)
    return obj