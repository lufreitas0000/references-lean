"""Jordan-Wigner Fock space construction on a centred finite band.

Centred band: -L/2 < n <= L/2 (length L, even L).
Vacuum state: all n <= 0 filled.
"""

from __future__ import annotations
import math
from typing import Set, Tuple, List, Dict, Optional
import numpy as np
import scipy.sparse as sp


def build_modes(L: int) -> List[int]:
    """Centred band modes: -L/2 < n <= L/2."""
    if L % 2 != 0:
        raise ValueError(f"L must be even, got {L}")
    return list(range(-L // 2 + 1, L // 2 + 1))


class FockSpace:
    """Sparse Jordan-Wigner Fock space for 1D fermions in a centred band."""

    def __init__(self, L: int):
        if L % 2 != 0 or L < 2:
            raise ValueError(f"L must be positive even integer, got {L}")
        self.L = L
        self.modes: List[int] = build_modes(L)
        self.D: int = len(self.modes)
        self.dim: int = 1 << self.D

        # Vac: modes <= 0 are occupied (first L//2 modes in our sorted list)
        self.vac_occ: Set[int] = {n for n in self.modes if n <= 0}
        self.P_vac: int = sum(self.vac_occ)
        self.vac_idx: int = self.occ_to_idx(self.vac_occ)

        # Jordan-Wigner single-site operators
        # Basis: |0> = empty, |1> = occupied
        # a|1> = |0>, a|0> = 0 => a = [[0, 1], [0, 0]]
        I2 = sp.identity(2, format="csr", dtype=float)
        Z = sp.diags([1.0, -1.0], format="csr", dtype=float)
        a = sp.csr_matrix([[0.0, 1.0], [0.0, 0.0]], dtype=float)

        def kron_all(matrices):
            out = matrices[0]
            for m in matrices[1:]:
                out = sp.kron(out, m, format="csr")
            return out

        self.c: Dict[int, sp.csr_matrix] = {}
        for i, n in enumerate(self.modes):
            ms = [Z] * i + [a] + [I2] * (self.D - i - 1)
            self.c[n] = kron_all(ms)

        self.cd: Dict[int, sp.csr_matrix] = {
            n: self.c[n].T.tocsr() for n in self.modes
        }

        # Number operators for each mode
        self.n_op: Dict[int, sp.csr_matrix] = {
            n: self.cd[n] @ self.c[n] for n in self.modes
        }

        # Global operators
        Id = sp.identity(self.dim, format="csr", dtype=float)
        self.N_op: sp.csr_matrix = (
            sum(self.n_op[n] for n in self.modes) - (self.L // 2) * Id
        )
        self.P_op: sp.csr_matrix = (
            sum(n * self.n_op[n] for n in self.modes) - self.P_vac * Id
        )
        # Energy operator: e = P - N(N+1)/2
        N_term = (self.N_op @ (self.N_op + Id)) * 0.5
        self.energy_op: sp.csr_matrix = self.P_op - N_term

        # Dense vacuum state vector
        self.vacuum = np.zeros(self.dim, dtype=float)
        self.vacuum[self.vac_idx] = 1.0

    def occ_to_idx(self, occ: Set[int]) -> int:
        """Convert a set of occupied modes to basis state index."""
        idx = 0
        for i, n in enumerate(self.modes):
            if n in occ:
                idx |= 1 << (self.D - 1 - i)
        return idx

    def idx_to_occ(self, idx: int) -> Set[int]:
        """Convert a basis state index to set of occupied modes."""
        return {
            self.modes[i]
            for i in range(self.D)
            if (idx >> (self.D - 1 - i)) & 1
        }

    def rho(self, m: int) -> sp.csr_matrix:
        """Current / density operator: rho(m) = sum_n c^dag_{n+m} c_n."""
        R = sp.csr_matrix((self.dim, self.dim), dtype=float)
        for n in self.modes:
            if (n + m) in self.modes:
                R = R + self.cd[n + m] @ self.c[n]
        return R

    def b(self, m: int) -> sp.csr_matrix:
        """Bosonic annihilation operator: b(m) = rho(-m) / sqrt(m) for m > 0."""
        if m <= 0:
            raise ValueError(f"m must be > 0, got {m}")
        return self.rho(-m) / math.sqrt(m)

    def bd(self, m: int) -> sp.csr_matrix:
        """Bosonic creation operator: b^dag(m) = rho(m) / sqrt(m) for m > 0."""
        if m <= 0:
            raise ValueError(f"m must be > 0, got {m}")
        return self.rho(m) / math.sqrt(m)

    def energy_from_occ(self, occ: Set[int]) -> Tuple[int, int, int]:
        """Compute (e, N, P) for an occupation set."""
        N = len(occ) - self.L // 2
        P = sum(occ) - self.P_vac
        e = P - N * (N + 1) // 2
        return e, N, P

    def all_energies(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Vectorized computation of (e, N, P) for all 2^D basis states."""
        idx = np.arange(self.dim)
        bits = ((idx[:, None] >> (self.D - 1 - np.arange(self.D))[None, :]) & 1)
        Ns = bits.sum(1) - self.L // 2
        mv = np.array(self.modes)
        Ps = bits @ mv - self.P_vac
        es = Ps - Ns * (Ns + 1) // 2
        return es, Ns, Ps

    def budget_indices(self, K: int, Nmax: int) -> np.ndarray:
        """Basis indices satisfying e <= K and |N| <= Nmax."""
        es, Ns, _ = self.all_energies()
        sel = np.where((es <= K) & (np.abs(Ns) <= Nmax))[0]
        return sel

    def budget_vecs(self, K: int, Nmax: int) -> sp.csr_matrix:
        """Isometry matrix V whose columns are the budget basis states."""
        sel = self.budget_indices(K, Nmax)
        k = len(sel)
        if k == 0:
            return sp.csr_matrix((self.dim, 0), dtype=float)
        return sp.csr_matrix(
            (np.ones(k, dtype=float), (sel, np.arange(k))),
            shape=(self.dim, k),
            dtype=float,
        )

    def sector_ground_state_occ(self, N: int) -> Set[int]:
        """Return occupation set for ground state of charge sector N."""
        k = self.L // 2 + N
        if not (0 <= k <= self.D):
            raise ValueError(f"Sector N={N} out of range for L={self.L}")
        return set(self.modes[:k])

    def deep_hole_occ(self, d: int) -> Set[int]:
        """Return state with a deep hole at depth d: remove mode n = -d from vacuum."""
        if not (0 <= d < self.L // 2):
            raise ValueError(f"Depth {d} out of range [0, {self.L // 2})")
        return self.vac_occ - {-d}
