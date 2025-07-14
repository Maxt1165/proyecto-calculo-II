import numpy as np
import sympy as sp

def calcular_gradiente(expresion, punto):
    """
    Calcula el vector gradiente en un punto dado para una función f(x,y)
    Args:
        expresion (str): Función matemática (ej: "x**2 + y**2")
        punto (tuple): Punto (x, y) donde calcular el gradiente 
    Returns:
        tuple: Vector gradiente (df/dx, df/dy)
    """
   # 1. Crear símbolos y expresión
    x, y = sp.symbols('x y')
    try:
        expr = sp.sympify(expresion)
    
        # 2. Calcular derivadas parciales
        df_dx = sp.diff(expr, x)
        df_dy = sp.diff(expr, y)
        
        # 3. Evaluar en el punto dado
        f_dx = df_dx.subs({x: punto[0], y: punto[1]})
        f_dy = df_dy.subs({x: punto[0], y: punto[1]})
        
        return (float(f_dx), float(f_dy))
    except (sp.SympifyError, TypeError):
        print(f"Expresión inválida: {expresion}")
        return None
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def vector_gradiente(funcion, dominio_x, dominio_y, resolucion=20):
    """
    Genera un campo vectorial del gradiente para visualización 
    Args:
        funcion (str): Función matemática
        dominio_x (tuple): Rango en X (min, max)
        dominio_y (tuple): Rango en Y (min, max)
        resolucion (int): Puntos por eje   
    Returns:
        list: Vectores en formato [(origen, vector), ...]
    """
    # Crear grid
    x = np.linspace(*dominio_x, resolucion)
    y = np.linspace(*dominio_y, resolucion)
    X, Y = np.meshgrid(x, y)
    
    vectores = []
    for i in range(resolucion):
        for j in range(resolucion):
            punto = (X[i,j], Y[i,j])
            grad = calcular_gradiente(funcion, punto)
            # Escalar vector para mejor visualización
            escala = 0.3
            vector_esc = (grad[0]*escala, grad[1]*escala, 0)
            vectores.append(((X[i,j], Y[i,j], 0), vector_esc))    
    return vectores