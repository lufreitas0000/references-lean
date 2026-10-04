"""Test Bosonic Fock space (polynomials in X_m)."""

import pytest
import sympy as sp


def test_bosonfock_commutation():
    """on polynomials in X_1..X_3, [d_m, X_m'] = delta, Euler operator = degree"""
    X1, X2, X3 = sp.symbols('X1 X2 X3')
    
    # Let d_m = d/dX_m
    # We test [d_m, X_m'] P = delta_{m,m'} P
    
    P = X1**2 * X2 + 3 * X2**3 * X3 - X1 * X3**2
    
    def comm_dX_X(m, mp, P):
        X = {1: X1, 2: X2, 3: X3}
        Xm = X[m]
        Xmp = X[mp]
        
        # d_m (X_{m'} P) - X_{m'} (d_m P)
        term1 = sp.diff(Xmp * P, Xm)
        term2 = Xmp * sp.diff(P, Xm)
        return sp.simplify(term1 - term2)
        
    for m in [1, 2, 3]:
        for mp in [1, 2, 3]:
            res = comm_dX_X(m, mp, P)
            if m == mp:
                assert sp.simplify(res - P) == 0
            else:
                assert sp.simplify(res) == 0


def test_bosonfock_euler():
    """Euler operator = degree"""
    X1, X2, X3 = sp.symbols('X1 X2 X3')
    
    # Euler operator E = sum_m X_m d/dX_m
    # E P = deg(P) P for homogeneous P
    
    P_deg3 = X1**3 + 2 * X1 * X2 * X3 + X3**3
    
    E_P = sp.simplify(X1 * sp.diff(P_deg3, X1) + X2 * sp.diff(P_deg3, X2) + X3 * sp.diff(P_deg3, X3))
    
    assert sp.simplify(E_P - 3 * P_deg3) == 0
    
    P_deg4 = X1**2 * X2**2 + X2 * X3**3
    E_P4 = sp.simplify(X1 * sp.diff(P_deg4, X1) + X2 * sp.diff(P_deg4, X2) + X3 * sp.diff(P_deg4, X3))
    assert sp.simplify(E_P4 - 4 * P_deg4) == 0
