"""Test umbral / finite-difference calculus using SymPy and Numpy."""

import pytest
import numpy as np
import sympy as sp
from umbral import E, Delta, beta, falling_factorial, umbral_map, newton_series_terms, summation_by_parts, telescoping_sum, shift_periodic


def test_leibniz_rule():
    """discrete Leibniz Delta(fg) = Delta f g + E f Delta g"""
    x = sp.Symbol('x')
    f = sp.Function('f')(x)
    g = sp.Function('g')(x)
    
    LHS = Delta(f * g, x)
    RHS = sp.simplify(Delta(f, x) * g + E(f, x) * Delta(g, x))
    assert sp.simplify(LHS - RHS) == 0


def test_summation_by_parts():
    """summation by parts on Z_L"""
    L = 10
    np.random.seed(42)
    f = np.random.randn(L)
    g = np.random.randn(L)
    lhs, rhs = summation_by_parts(f, g)
    assert np.isclose(lhs, rhs)


def test_telescoping():
    """telescoping; sum_{x=a}^{b-1} (Delta v)[x] = v[b] - v[a]"""
    L = 10
    np.random.seed(43)
    v = np.random.randn(L)
    for a in range(L):
        for b in range(a + 1, L):
            lhs, expected = telescoping_sum(v, a, b)
            assert np.isclose(lhs, expected)


def test_delta_falling_factorial():
    """Delta x^(n falling) = n x^(n-1 falling)"""
    x = sp.Symbol('x')
    for n in range(1, 5):
        ff_n = falling_factorial(x, n)
        ff_n_minus_1 = falling_factorial(x, n - 1)
        lhs = Delta(ff_n, x)
        rhs = n * ff_n_minus_1
        assert sp.simplify(lhs - rhs) == 0


def test_umbral_map_intertwines():
    """umbral map intertwines d/dx and Delta"""
    x = sp.Symbol('x')
    # Test on a polynomial
    P = 3 * x**3 - 2 * x**2 + 5 * x - 7
    
    # Delta(umbral_map(P(x)))
    mapped_P = umbral_map(P, x)
    lhs = Delta(mapped_P, x)
    
    # umbral_map(d/dx P(x))
    dP = sp.diff(P, x)
    rhs = umbral_map(dP, x)
    
    assert sp.simplify(lhs - rhs) == 0


def test_delta_beta_commutator():
    """[Delta, beta] = 1 on functions"""
    x = sp.Symbol('x')
    f = sp.Function('f')(x)
    
    # Delta(beta(f)) - beta(Delta(f))
    b_f = beta(f, x)
    D_b_f = Delta(b_f, x)
    
    D_f = Delta(f, x)
    b_D_f = beta(D_f, x)
    
    comm = sp.simplify(D_b_f - b_D_f)
    assert sp.simplify(comm - f) == 0


def test_newton_series():
    """Newton series E^n = sum C(n,k) Delta^k"""
    x = sp.Symbol('x')
    f = sp.Function('f')(x)
    
    for n in range(1, 4):
        lhs = E(f, x, n)
        rhs = newton_series_terms(f, x, n)
        assert sp.simplify(lhs - rhs) == 0
