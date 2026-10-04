"""Umbral (finite-difference) calculus with SymPy and discrete lattice operations.

Provides:
- Shift operator E: E f(x) = f(x + 1)
- Forward difference Delta: Delta f(x) = f(x + 1) - f(x)
- Backward difference nabla: nabla f(x) = f(x) - f(x - 1)
- Oscillator creation operator beta: beta f(x) = x f(x - 1)
- Falling factorial x^(n falling) = x(x-1)...(x-n+1)
- Umbral map: X^n |-> x^(n falling) intertwining d/dx and Delta
- Newton series: E^n = sum_k binom(n, k) Delta^k
- Discrete summation by parts and telescoping on Z_L
"""

from __future__ import annotations
import math
from typing import Callable, Union, Sequence
import numpy as np
import sympy as sp


def E(f: sp.Expr, x: sp.Symbol, h: Union[int, sp.Expr] = 1) -> sp.Expr:
    """Shift operator: E^h f(x) = f(x + h)."""
    return f.subs(x, x + h)


def Delta(f: sp.Expr, x: sp.Symbol, h: Union[int, sp.Expr] = 1) -> sp.Expr:
    """Forward difference operator: Delta_h f(x) = f(x + h) - f(x)."""
    return sp.simplify(E(f, x, h) - f)


def nabla(f: sp.Expr, x: sp.Symbol, h: Union[int, sp.Expr] = 1) -> sp.Expr:
    """Backward difference operator: nabla_h f(x) = f(x) - f(x - h)."""
    return sp.simplify(f - E(f, x, -h))


def beta(f: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Creation operator for discrete oscillator: beta f(x) = x f(x - 1)."""
    return sp.simplify(x * E(f, x, -1))


def falling_factorial(x: Union[sp.Symbol, sp.Expr, int], n: int) -> sp.Expr:
    """Falling factorial x^(n falling) = prod_{i=0}^{n-1} (x - i).

    For n = 0, returns 1.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative integer, got {n}")
    if n == 0:
        return sp.Integer(1)
    res = sp.Integer(1)
    for i in range(n):
        res = res * (x - i)
    return sp.simplify(res)


def umbral_map(expr: sp.Expr, x: sp.Symbol, target: sp.Symbol | None = None) -> sp.Expr:
    """Umbral map: replaces x^k with falling_factorial(target or x, k).

    Intertwines d/dx and Delta:
        Delta(umbral_map(P(x))) = umbral_map(d/dx P(x))
    """
    tgt = target if target is not None else x
    p = sp.Poly(expr, x)
    res = sp.Integer(0)
    for monom, coeff in p.terms():
        k = monom[0]
        res = res + coeff * falling_factorial(tgt, k)
    return sp.simplify(res)


def newton_series_terms(f: sp.Expr, x: sp.Symbol, n: int) -> sp.Expr:
    """Evaluate Newton series sum_{k=0}^n binom(n, k) Delta^k f(x)."""
    current_diff = f
    res = sp.Integer(0)
    for k in range(n + 1):
        coeff = sp.binomial(n, k)
        res = res + coeff * current_diff
        current_diff = Delta(current_diff, x)
    return sp.simplify(res)


# Lattice / periodic functions on Z_L (represented as 1D numpy arrays)

def shift_periodic(v: np.ndarray, h: int = 1) -> np.ndarray:
    """Periodic shift: (E^h v)[x] = v[(x + h) % L]."""
    return np.roll(v, -h)


def delta_periodic(v: np.ndarray) -> np.ndarray:
    """Periodic forward difference: Delta v = E v - v."""
    return shift_periodic(v, 1) - v


def nabla_periodic(v: np.ndarray) -> np.ndarray:
    """Periodic backward difference: nabla v = v - E^(-1) v."""
    return v - shift_periodic(v, -1)


def summation_by_parts(f: np.ndarray, g: np.ndarray) -> Tuple[float, float]:
    """Verify summation by parts on Z_L:

    sum (Delta f) * g == - sum (E f) * (Delta g).
    Returns (sum(Delta(f) * g), -sum(E(f) * Delta(g))).
    """
    lhs = float(np.sum(delta_periodic(f) * g))
    rhs = float(-np.sum(shift_periodic(f, 1) * delta_periodic(g)))
    return lhs, rhs


def telescoping_sum(v: np.ndarray, a: int, b: int) -> Tuple[float, float]:
    """Verify telescoping: sum_{x=a}^{b-1} (Delta v)[x] = v[b] - v[a]."""
    diff = np.roll(v, -1) - v
    s = float(np.sum(diff[a:b]))
    expected = float(v[b] - v[a])
    return s, expected
