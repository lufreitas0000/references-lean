Here is the detailed, mathematically rigorous formalism for Chapter 6 of the mathematical physics document.

***

# Chapter 6: Subspace Formalism and the Energy Budget

In this chapter, we rigorously establish the foundation for the fermionic Fock space on a finite 1D lattice of size $L$ (where $L \in 2\mathbb{N}$). We define the Dirac vacuum, the $U(1)$ charge (number) sectors, normal ordering, and the energy budget truncation scheme. This machinery is necessary to formalize Hamiltonian truncation and duality mappings on the lattice.

Let the lattice momentum indices be denoted by the set $\mathcal{I} = \{-L/2 + 1, \dots, L/2\}$. A fermionic Fock state is uniquely characterized by a subset $S \subseteq \mathcal{I}$ of occupied modes. The full Fock space is $\mathcal{F} = \mathrm{span}\{|S\rangle \mid S \subseteq \mathcal{I}\}$.

---

## 1.7 Vacuum, Number, and Normal Ordering

### Definitions

**Definition 6.1 (Dirac Vacuum)**
`\leanref{Bosonize.Core.vacuum_state}`
The vacuum state $|\Omega\rangle$ is defined as the basis state corresponding to the fully occupied Dirac sea up to $n=0$. Its subset of occupied modes is:
$$ S_\Omega = \mathcal{I}_{\le 0} = \{n \in \mathcal{I} \mid n \le 0\} $$
A mode $n$ in the vacuum is occupied if and only if $n \le 0$.

**Definition 6.2 (Sector Number)**
`\leanref{Bosonize.Core.sector_number}`
For any configuration $S \subseteq \mathcal{I}$, the sector number (or net charge) is defined as:
$$ N(S) = |S| - \frac{L}{2} $$
The corresponding self-adjoint number operator on $\mathcal{F}$ is:
$$ \hat N = \sum_{n \in \mathcal{I}} (\hat n_n - \langle \Omega | \hat n_n | \Omega \rangle) = \sum_{n \in \mathcal{I}} (\hat n_n - \chi_{\le 0}(n)) $$
where $\hat n_n = c^\dagger_n c_n$ and $\chi_{\le 0}(n)$ is the indicator function for $n \le 0$.

**Definition 6.3 (Normal Ordering)**
`\leanref{Bosonize.Core.normal_order_bilinear}`
The normal ordering of a fermionic bilinear relative to the Dirac vacuum $\Omega$ is defined explicitly as:
$$ :\!c^\dagger_a c_b\!: \ = c^\dagger_a c_b - \delta_{a,b}\chi_{\le 0}(a) $$

**Definition 6.4 (Sector Ground States)**
`\leanref{Bosonize.Core.sector_ground_state}`
For any integer $N$ such that $-L/2 \le N \le L/2$, the sector ground state $|N\rangle_0$ is defined as the basis state corresponding to the subset:
$$ S_{N,0} = \{n \in \mathcal{I} \mid n \le N\} $$
We adopt the canonical phase convention such that $|S\rangle$ is formed by acting with $c_n^\dagger$ in strictly descending order of $n$. Hence:
$$ |N\rangle_0 = \begin{cases} 
c^\dagger_N c^\dagger_{N-1} \dots c^\dagger_1 |\Omega\rangle & \text{if } N > 0 \\
c_0 c_{-1} \dots c_{N+1} |\Omega\rangle & \text{if } N < 0 \\
|\Omega\rangle & \text{if } N = 0 
\end{cases} $$

### Theorems

**Theorem 6.5 (Vacuum Expectation of Normal Ordered Bilinears)**
`\leanref{Bosonize.Core.vacuum_exp_normal_order_zero}`
For any $a, b \in \mathcal{I}$, the vacuum expectation value of the normal-ordered bilinear vanishes:
$$ \langle \Omega | :\!c^\dagger_a c_b\!: | \Omega \rangle = 0 $$

**Theorem 6.6 (Sector Ground State Properties)**
`\leanref{Bosonize.Core.sector_ground_state_props}`
The set of sector ground states $\{|N\rangle_0\}_{N = -L/2}^{L/2}$ forms an orthonormal family. Furthermore, each $|N\rangle_0$ is an eigenstate of the number operator:
$$ \hat N |N\rangle_0 = N |N\rangle_0 $$

### Proofs

*Proof of Theorem 6.5.*
Evaluate the expectation value using the definition of the vacuum:
$$ \langle \Omega | c^\dagger_a c_b | \Omega \rangle = \delta_{a,b} \langle \Omega | \hat n_a | \Omega \rangle = \delta_{a,b} \chi_{\le 0}(a) $$
Substituting this into Definition 6.3 yields:
$$ \langle \Omega | :\!c^\dagger_a c_b\!: | \Omega \rangle = \delta_{a,b} \chi_{\le 0}(a) - \delta_{a,b} \chi_{\le 0}(a) = 0 $$
$\blacksquare$

*Proof of Theorem 6.6.*
Orthonormality follows immediately from the fact that distinct $N$ define distinct subsets $S_{N,0} \neq S_{M,0}$, and Fock states associated with distinct subsets are orthogonal.
For the eigenvalue equation, evaluate $\hat N$ on $|N\rangle_0$. By definition, the occupied set is $S_{N,0}$. Thus, the expectation of $\hat N$ is:
$$ \sum_{n \in S_{N,0}} 1 - \sum_{n \in S_\Omega} 1 = |S_{N,0}| - |S_\Omega| = \left(\frac{L}{2} + N\right) - \frac{L}{2} = N $$
Since $|N\rangle_0$ is a basis state, it is an eigenstate of the diagonal operator $\hat N$ with eigenvalue $N$. $\blacksquare$

### *Continuum interpretation (not formalized)*
In the continuum limit $L \to \infty$, the discrete Dirac sea becomes an infinitely deep Fermi sea. The operators $c_n$ transition to continuous field modes, and the bare number operator $\sum \hat n_n$ diverges. Normal ordering relative to the physical vacuum becomes strictly necessary to yield a finite, measurable $U(1)$ charge. The sector ground states $|N\rangle_0$ represent the primary states of the $U(1)$ Kac-Moody algebra with definite topological charge.

---

## 1.8 Energy and Budget

### Definitions

**Definition 6.7 (Momentum/Bare Energy)**
`\leanref{Bosonize.Core.bare_energy}`
The relative momentum (or bare energy) of a configuration $S$ with respect to the vacuum is:
$$ P(S) = \sum_{n \in S} n - \sum_{n \le 0} n $$

**Definition 6.8 (Excitation Energy)**
`\leanref{Bosonize.Core.excitation_energy}`
The true excitation energy of a configuration $S$ relative to its own sector ground state is defined over the integers via the relation:
$$ 2 \cdot e(S) = 2 P(S) - N(S)(N(S)+1) $$
*(Equivalently, $e(S) = P(S) - \frac{N(N+1)}{2}$).*

**Definition 6.9 (Energy Budget Subspace)**
`\leanref{Bosonize.Core.budget_subspace}`
For non-negative integers $K$ and $N_{max}$, the budget subspace $\mathcal{B}_{K, N_{max}}$ is defined as:
$$ \mathcal{B}_{K, N_{max}} = \mathrm{span} \{ |S\rangle \mid e(S) \le K \land |N(S)| \le N_{max} \} $$
We denote the orthogonal projector onto this subspace as $P_K$.

### Theorems

**Theorem 6.10 (Non-negativity and Ground State Identity)**
`\leanref{Bosonize.Core.energy_nonneg}` and `\leanref{Bosonize.Core.energy_zero_iff_gs}`
For any configuration $S \subseteq \mathcal{I}$:
1. $e(S) \ge 0$.
2. $e(S) = 0 \iff S = S_{N(S),0}$.

**Theorem 6.11 (Deep Hole / Particle Excitations)**
`\leanref{Bosonize.Core.hole_particle_energy}`
Let $S_{N,0}$ be a sector ground state. 
- Removing a particle (creating a hole) at depth $d \ge 0$ below the Fermi surface, i.e., at $n = N - d$, yields a state $S'$ with $N(S') = N-1$ and $e(S') = d$.
- Adding a particle at height $h \ge 1$ above the Fermi surface, i.e., at $n = N + h$, yields a state $S'$ with $N(S') = N+1$ and $e(S') = h-1$.

**Lemma 6.12 (Energy Shift Lemmas)**
`\leanref{Bosonize.Core.energy_shift_create}` and `\leanref{Bosonize.Core.energy_shift_annihilate}`
Let $S \subseteq \mathcal{I}$ have sector number $N$.
1. If $n \notin S$ and $S' = S \cup \{n\}$, then $e(S') = e(S) + n - (N + 1)$.
2. If $n \in S$ and $S' = S \setminus \{n\}$, then $e(S') = e(S) - n + N$.

### Proofs

*Proof of Theorem 6.10.*
Fix $N = N(S)$. The minimum possible value of $P(S)$ for a fixed cardinality $|S| = L/2 + N$ is achieved by packing the lowest available integers. The configuration that accomplishes this is precisely $S_{N,0}$.
For $S_{N,0}$ (assuming $N \ge 0$ for brevity; the $N < 0$ case is symmetric), the bare energy is:
$$ P(S_{N,0}) = \sum_{n=1}^N n = \frac{N(N+1)}{2} $$
Therefore, $\min P(S) = \frac{N(N+1)}{2}$, implying $e(S) = P(S) - \frac{N(N+1)}{2} \ge 0$.
Equality holds if and only if the integers in $S$ are perfectly packed, which uniquely identifies $S$ as $S_{N,0}$. $\blacksquare$

*Proof of Lemma 6.12.*
Consider the creation of a particle: $S' = S \cup \{n\}$. By definition, $N(S') = N + 1$ and $P(S') = P(S) + n$.
Substitute these into the definition of excitation energy (Def 6.8):
$$ e(S') = P(S') - \frac{N(S')(N(S') + 1)}{2} $$
$$ e(S') = P(S) + n - \frac{(N+1)(N+2)}{2} $$
Expand the fraction:
$$ \frac{(N+1)(N+2)}{2} = \frac{N(N+1)}{2} + N + 1 $$
Substituting this back yields:
$$ e(S') = \left(P(S) - \frac{N(N+1)}{2}\right) + n - (N + 1) = e(S) + n - (N + 1) $$
The proof for annihilation (part 2) follows an identical algebraic procedure, setting $N(S') = N - 1$ and $P(S') = P(S) - n$. $\blacksquare$

*Proof of Theorem 6.11.*
We apply Lemma 6.12 to the sector ground state $S_{N,0}$, which by Theorem 6.10 has $e(S_{N,0}) = 0$.
For a deep hole, we remove $n = N - d$. Using part 2 of the Shift Lemma:
$$ e(S') = 0 - (N - d) + N = d $$
For a new particle, we add $n = N + h$. Using part 1 of the Shift Lemma:
$$ e(S') = 0 + (N + h) - (N + 1) = h - 1 $$
$\blacksquare$

### *Continuum interpretation (not formalized)*
The bare energy $P(S)$ maps directly to the chiral momentum (or the Virasoro generator $L_0$) in the corresponding Conformal Field Theory (CFT). The quantity $\frac{N(N+1)}{2}$ represents the minimal conformal weight of the charge-$N$ vertex operator in the bosonized theory. Consequently, $e(S)$ measures the strict integer-spaced energy spectrum of descendants above the primary field. The budget subspace $\mathcal{B}_{K, N_{max}}$ implements an exact Hamiltonian truncation (Truncated Conformal Space Approach, or TCSA). Because $e(S)$ is bounded below, operators dynamically mapped under duality are guaranteed to remain within well-behaved finite-dimensional subspaces when governed by $P_K$, allowing robust numerical and algebraic convergence limits.