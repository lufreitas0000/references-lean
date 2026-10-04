"""Test canonical anticommutation relations (CAR) for Jordan-Wigner fermions."""

import pytest
import numpy as np
import scipy.sparse as sp
from fock import FockSpace


@pytest.mark.parametrize("L", [4, 6])
def test_car_anticommutator_c_cdag(L):
    """Test {c_n, c_p^dag} = delta_{n, p} * I for all pairs n, p."""
    fock = FockSpace(L)
    Id = sp.identity(fock.dim, format="csr", dtype=float)
    for n in fock.modes:
        for p in fock.modes:
            anti = fock.c[n] @ fock.cd[p] + fock.cd[p] @ fock.c[n]
            if n == p:
                diff = anti - Id
            else:
                diff = anti
            assert diff.nnz == 0 or np.abs(diff.data).max() < 1e-12


@pytest.mark.parametrize("L", [4, 6])
def test_car_anticommutator_c_c(L):
    """Test {c_n, c_p} = 0 for all pairs n, p."""
    fock = FockSpace(L)
    for n in fock.modes:
        for p in fock.modes:
            anti = fock.c[n] @ fock.c[p] + fock.c[p] @ fock.c[n]
            assert anti.nnz == 0 or np.abs(anti.data).max() < 1e-12


@pytest.mark.parametrize("L", [4, 6])
def test_car_anticommutator_cdag_cdag(L):
    """Test {c_n^dag, c_p^dag} = 0 for all pairs n, p."""
    fock = FockSpace(L)
    for n in fock.modes:
        for p in fock.modes:
            anti = fock.cd[n] @ fock.cd[p] + fock.cd[p] @ fock.cd[n]
            assert anti.nnz == 0 or np.abs(anti.data).max() < 1e-12
