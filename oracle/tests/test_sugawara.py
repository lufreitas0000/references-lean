"""Test Sugawara construction: P - N(N+1)/2 = sum_m m b_m^dag b_m on the budget."""

import pytest
import numpy as np
import scipy.sparse as sp
from fock import FockSpace


@pytest.mark.parametrize("L", [6, 8])
def test_sugawara_energy_identity_on_budget(L):
    """Verify Pop = P - N(N+1)/2 equals S = sum_m m b_m^dag b_m on low-energy budget."""
    fock = FockSpace(L)
    # Sugawara operator S = sum_{m=1}^{L//2 - 1} m b_m^dag b_m
    # Note m b_m^dag b_m = rho(m) @ rho(-m)
    S = sp.csr_matrix((fock.dim, fock.dim), dtype=float)
    for m in range(1, L // 2):
        S = S + fock.rho(m) @ fock.rho(-m)

    Pop = fock.energy_op

    # Test for low-energy budget states where Sugawara holds exactly
    # For small K, Nmax within the truncation window
    for Nmax in [0, 1]:
        for K in range(0, 3):
            # Budget window requires enough modes not to hit boundary: K + Nmax < L//2
            if K + Nmax >= L // 2:
                continue
            V = fock.budget_vecs(K, Nmax)
            if V.shape[1] == 0:
                continue
            diff = (Pop - S) @ V
            max_err = np.abs(diff.data).max() if diff.nnz > 0 else 0.0
            assert max_err < 1e-9, (
                f"L={L}, K={K}, Nmax={Nmax}: Sugawara violation = {max_err}"
            )


def test_sugawara_on_vacuum():
    """Vacuum has P = 0, N = 0, so Pop|vac> = 0 and S|vac> = 0."""
    fock = FockSpace(8)
    vac = fock.vacuum
    S = sp.csr_matrix((fock.dim, fock.dim), dtype=float)
    for m in range(1, fock.L // 2):
        S = S + fock.rho(m) @ fock.rho(-m)

    pop_vac = fock.energy_op @ vac
    s_vac = S @ vac
    assert np.allclose(pop_vac, 0.0)
    assert np.allclose(s_vac, 0.0)


def test_sugawara_single_boson_state():
    """State |m> = b_m^dag |vac> = rho(m)/sqrt(m) |vac> has energy e = m."""
    fock = FockSpace(8)
    vac = fock.vacuum
    for m in [1, 2, 3]:
        # Create single boson state
        state = (fock.rho(m) @ vac) / np.sqrt(m)
        norm = np.linalg.norm(state)
        assert abs(norm - 1.0) < 1e-9

        # Pop should have eigenvalue m
        applied = fock.energy_op @ state
        assert np.allclose(applied, m * state)
