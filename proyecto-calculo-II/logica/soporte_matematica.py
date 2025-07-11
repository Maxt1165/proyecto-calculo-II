import sympy as sp
import numpy as np
import re

def safe_lambdify(expression):
    """Crea función numérica segura para Blender 4.4.3"""
    # Limpiar expresión para seguridad
    limpiar_expr = re.sub(r'[^0-9a-zA-Z\+\-\*\/\^\(\)\.]', '', expression)
    
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
    
