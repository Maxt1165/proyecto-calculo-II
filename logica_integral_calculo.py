import sympy as sp

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
