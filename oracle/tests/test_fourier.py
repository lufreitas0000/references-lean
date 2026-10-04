"""Test Fourier transform properties."""

import pytest
import numpy as np


@pytest.mark.parametrize("L", [4, 6, 8])
def test_fourier_orthogonality(L):
    """orthogonality sum_x zeta^((k-k')x) = L delta"""
    zeta = np.exp(2j * np.pi / L)
    for k in range(L):
        for kp in range(L):
            s = sum(zeta ** ((k - kp) * x) for x in range(L))
            if k == kp:
                assert np.isclose(s, L)
            else:
                assert np.isclose(s, 0)


@pytest.mark.parametrize("L", [4, 6, 8])
def test_fourier_delta_eigenvector(L):
    """Delta e_k = (zeta^k - 1) e_k"""
    zeta = np.exp(2j * np.pi / L)
    for k in range(L):
        # e_k[x] = zeta^(k x)
        ek = np.array([zeta ** (k * x) for x in range(L)])
        # Delta e_k = E e_k - e_k
        E_ek = np.roll(ek, -1)
        Delta_ek = E_ek - ek
        expected = (zeta ** k - 1) * ek
        assert np.allclose(Delta_ek, expected)


@pytest.mark.parametrize("L", [4, 6, 8])
def test_fourier_unitary(L):
    """DFT unitary."""
    omega = np.exp(2j * np.pi / L)
    F = np.array([[omega ** (j * k) for k in range(L)] for j in range(L)]) / np.sqrt(L)
    assert np.allclose(F @ F.conj().T, np.eye(L))
    assert np.allclose(F.conj().T @ F, np.eye(L))
