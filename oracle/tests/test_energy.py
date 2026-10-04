"""Test fermion energy spectrum: positivity, sector ground states, deep holes."""

import pytest
import numpy as np
from fock import FockSpace


@pytest.mark.parametrize("L", [4, 6, 8, 10])
def test_energy_non_negative(L):
    """e(S) >= 0 for all basis states S in the centred band."""
    fock = FockSpace(L)
    es, _, _ = fock.all_energies()
    assert np.all(es >= 0), f"Found negative energy for L={L}: min={es.min()}"


@pytest.mark.parametrize("L", [4, 6, 8, 10])
def test_sector_ground_state_uniqueness(L):
    """e(S) == 0 iff S is the sector ground state (filling lowest L/2 + N modes)."""
    fock = FockSpace(L)
    es, Ns, _ = fock.all_energies()

    zero_indices = np.where(es == 0)[0]
    expected_indices = []

    # For each allowed charge N in [-L//2, L//2]
    for N in range(-L // 2, L // 2 + 1):
        gs_occ = fock.sector_ground_state_occ(N)
        idx = fock.occ_to_idx(gs_occ)
        expected_indices.append(idx)
        # Verify gs has e = 0
        e, n_sec, p_sec = fock.energy_from_occ(gs_occ)
        assert n_sec == N
        assert e == 0, f"Sector {N} ground state has non-zero energy {e}"

    # Exactly one state with e=0 per sector
    assert set(zero_indices) == set(expected_indices)
    assert len(zero_indices) == L + 1


@pytest.mark.parametrize("L", [4, 6, 8, 10])
def test_deep_hole_energies(L):
    """Removing mode n = -d from vacuum gives sector N = -1 and energy e = d."""
    fock = FockSpace(L)
    for d in range(L // 2):
        occ = fock.deep_hole_occ(d)
        e, N, P = fock.energy_from_occ(occ)
        assert N == -1, f"Expected sector N=-1, got N={N}"
        assert e == d, f"Expected energy e={d}, got e={e}"
