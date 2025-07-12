import sympy as sp
print('Se importó sympy en el archivo soporte_matematica')
import numpy as np #evaluar la función de forma vectorizada sobre la malla
print('Se importó numpy en el archivo soporte_matematica')
import re #Para hacer limpieza de caracteres peligrosos en la expresión.
print('Se importó ¿re? en el archivo soporte_matematica')

"""Propósito: Convertir una expresión escrita por el usuario como "x**2 + y**2" en una
# función evaluable en NumPy, de forma segura, tolerante a errores y compatible con Blender"""
def hacerfuncion_segura(expresion):
    # Limpiar expresión para seguridad:soloacepta,numeros,letras,operadores, parentesis
    limpiar_expr = re.sub(r'[^0-9a-zA-Z\+\-\*\/\^\(\)\.]', '', expresion)
    
    try:
        # Convertir a expresión simbólica
        x, y = sp.symbols('x y') #Define variables simbólicas
        expr = sp.sympify(limpiar_expr)#Convierte la cadena a una expresión simbólica
        
        # Crear función vectorizada
        f = sp.lambdify((x, y), expr, modules='numpy') #La convierte en función evaluable usando lambdify con backend numpy
        
#Manejar errores de dominio
        def hacerdominio_seguro(X, Y):
            with np.errstate(all='ignore'):
                result = f(X, Y)
                return np.nan_to_num(result, nan=0.0, posinf=10, neginf=-10)
                
        return hacerdominio_seguro
    
    #Si la expresión es inválida (por ejemplo, "import os" o "@@@x"), 
    # se devuelve una función nula f(x,y)=0, evitando que el sistema falle
    except Exception as e:
        def error_func(X, Y):
            return np.zeros_like(X)    
        return error_func
    
