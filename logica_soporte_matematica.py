import sympy as sp
print('Se importó sympy en el archivo soporte_matematica')
import numpy as np #evaluar la función de forma vectorizada sobre la malla
print('Se importó numpy en el archivo soporte_matematica')
import re #Para hacer limpieza de caracteres peligrosos en la expresión.
print('Se importó ¿re? en el archivo soporte_matematica')


"""Propósito: Convertir una expresión escrita por el usuario como "x**2 + y**2" en una
# función evaluable en NumPy, de forma segura, tolerante a errores y compatible con Blender"""
def safe_lambdify(expresion):
    # Limpiar expresión para seguridad
    limpiar_expr = re.sub(r'[^0-9a-zA-Z\+\-\*\/\^\(\)\.]', '', expresion)
    
    try:
        # Convertir a expresión simbólica
        x, y = sp.symbols('x y')
        expr = sp.sympify(limpiar_expr)
        
        # Crear función vectorizada
        f = sp.lambdify((x, y), expr, modules='numpy')
        
        # Manejar errores de dominio
        def safe_eval(X, Y):
            with np.errstate(all='ignore'):
                result = f(X, Y)
                return np.nan_to_num(result, nan=0.0, posinf=10, neginf=-10)
                
        return safe_eval
        
    except Exception as e:
        # Función de respaldo
        def error_func(X, Y):
            return np.zeros_like(X)
        
        return error_func
    
