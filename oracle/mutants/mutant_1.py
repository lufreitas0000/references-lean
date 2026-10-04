import sympy as sp
from umbral import Delta

def check():
    x = sp.Symbol('x')
    f = sp.Function('f')(x)
    g = sp.Function('g')(x)
    
    LHS = Delta(f * g, x)
    RHS = Delta(f, x) * g + f * Delta(g, x)
    
    return sp.simplify(LHS - RHS) == 0
