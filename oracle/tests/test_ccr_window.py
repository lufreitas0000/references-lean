"""Test CCR [rho(-m), rho(m)] = m on budget subspaces satisfying the window."""

import pytest
import numpy as np
import scipy.sparse as sp
from fock import FockSpace


@pytest.mark.parametrize("L", [8, 10])
def test_ccr_window_holds(L):
    """[rho(-m), rho(m')] = m * delta_{m, m'} on budget satisfying m, m' <= L/2 - K - |N|."""
    fock = FockSpace(L)
    Id = sp.identity(fock.dim, format="csr", dtype=float)

    for Nmax in [0, 1]:
        for K in range(0, 3):
            window = L // 2 - K - Nmax
            if window < 1:
                continue
            V = fock.budget_vecs(K, Nmax)
            if V.shape[1] == 0:
                continue

            for m in range(1, window + 1):
                for mp in range(1, window + 1):
                    # Commutator [rho(-m), rho(mp)]
                    comm = fock.rho(-m) @ fock.rho(mp) - fock.rho(mp) @ fock.rho(-m)
                    tgt = (m if m == mp else 0.0) * Id
                    diff = (comm - tgt) @ V
                    max_err = np.abs(diff.data).max() if diff.nnz > 0 else 0.0
                    assert max_err < 1e-8, (
                        f"L={L}, K={K}, Nmax={Nmax}, m={m}, mp={mp}: "
                        f"expected CCR inside window {window}, got error {max_err}"
                    )


@pytest.mark.parametrize("L", [8, 10])
def test_ccr_window_fails_outside(L):
    """CCR fails when m is strictly outside the window L/2 - K - |N|."""
    fock = FockSpace(L)
    Id = sp.identity(fock.dim, format="csr", dtype=float)

    # Pick K, Nmax where window is strictly less than L//2
    # e.g. K = 1, Nmax = 1 => window = L//2 - 2
    # Then m = L//2 is outside the window
    K = 1
    Nmax = 1
    window = L // 2 - K - Nmax
    assert window < L // 2

    V = fock.budget_vecs(K, Nmax)
    assert V.shape[1] > 0

    # m = L // 2 is well outside window
    m = L // 2
    comm = fock.rho(-m) @ fock.rho(m) - fock.rho(m) @ fock.rho(-m)
    diff = (comm - m * Id) @ V
    max_err = np.abs(diff.data).max() if diff.nnz > 0 else 0.0
    assert max_err > 0.1, (
        f"L={L}: expected CCR to fail outside window for m={m}, but max_err={max_err}"
    )


def test_vacuum_ccr_expectation():
    """Verify <vac|[rho(-m), rho(m)]|vac> = m and <vac|[rho(m), rho(-m)]|vac> = -m."""
    fock = FockSpace(6)
    vac = fock.vacuum
    for m in [1, 2, 3]:
        comm_minus_plus = fock.rho(-m) @ fock.rho(m) - fock.rho(m) @ fock.rho(-m)
        val = float(vac @ (comm_minus_plus @ vac))
        assert abs(val - m) < 1e-9

        comm_plus_minus = fock.rho(m) @ fock.rho(-m) - fock.rho(-m) @ fock.rho(m)
        val_opp = float(vac @ (comm_plus_minus @ vac))
        assert abs(val_opp - (-m)) < 1e-9
