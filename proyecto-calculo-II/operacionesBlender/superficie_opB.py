#Creación de superficies

#Dada una función matemática z = f(x, y), generar una una malla (grid) que represente esa superficie en el espacio 3D.
"""PASOS
1. Definir la función: El usuario ingresa una cadena (string) con la expresión matemática, por ejemplo: `"x**2 + y**2"`.
2. Definir el dominio: Rango para `x` y `y` (por ejemplo, `x` de -5 a 5, `y` de -5 a 5) y la resolución (número de puntos).
3. Evaluar la función: Para cada punto `(x, y)` en el dominio, calcular `z = f(x, y)`.
4. Crear la malla: Construir una malla de vértices y caras (quadrados o triángulos) que represente la superficie.
5. Añadir el objeto a la escena de Blender """