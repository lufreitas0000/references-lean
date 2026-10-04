Here is the detailed, mathematically rigorous section for your notes, formatted in standard Markdown with LaTeX math environments.

***

## Position and Momentum Fermions

In this section, we establish the rigorously defined discrete fermionic spaces. Let $L \in \mathbb{N}$ be the number of lattice sites. We define the index sets for position and momentum respectively as $\text{Site}_L = \mathbb{Z} / L\mathbb{Z}$ and $\text{Mode}_L = \mathbb{Z} / L\mathbb{Z}$. 

Let us assume a set of fundamental momentum-space fermionic annihilation and creation operators $\{c_n, c_n^\dagger\}_{n \in \text{Mode}_L}$ that satisfy the standard Canonical Anticommutation Relations (CAR):
$$
\{c_m, c_n^\dagger\} = \delta_{m,n}, \quad \{c_m, c_n\} = 0, \quad \{c_m^\dagger, c_n^\dagger\} = 0
$$

**Definition 1 (Position Basis Fermions).** We define the position-basis fermion operators $c_j$ for $j \in \text{Site}_L$ via the discrete Fourier transform (DFT):
$$
c_j = \frac{1}{\sqrt{L}} \sum_{n \in \text{Mode}_L} \zeta^{nj} c_n
$$
where $\zeta = \exp(i 2\pi / L)$ is the primitive $L$-th root of unity. The corresponding creation operator is given by the Hermitian adjoint:
$$
c_j^\dagger = \frac{1}{\sqrt{L}} \sum_{n \in \text{Mode}_L} \zeta^{-nj} c_n^\dagger
$$

**Theorem 1 (Canonical Anticommutation Relations in Position Basis).** *The position-basis operators satisfy the CAR: $\{c_j, c_k^\dagger\} = \delta_{j,k}$ and $\{c_j, c_k\} = 0$.*

*Proof.* By direct substitution of the definition and leveraging the bilinearity of the anticommutator:
$$
\{c_j, c_k^\dagger\} = \frac{1}{L} \sum_{m \in \text{Mode}_L} \sum_{n \in \text{Mode}_L} \zeta^{mj} \zeta^{-nk} \{c_m, c_n^\dagger\}
$$
Using the momentum-space CAR $\{c_m, c_n^\dagger\} = \delta_{m,n}$, the double sum collapses to a single sum:
$$
\{c_j, c_k^\dagger\} = \frac{1}{L} \sum_{n \in \text{Mode}_L} \zeta^{n(j-k)}
$$
By the unitarity of the finite Fourier transform (the fundamental orthogonality property of the roots of unity), $\frac{1}{L} \sum_{n=0}^{L-1} \zeta^{nx} = \delta_{x, 0 \pmod L}$. Thus:
$$
\{c_j, c_k^\dagger\} = \delta_{j,k}
$$
The proof for $\{c_j, c_k\} = 0$ follows identically from $\{c_m, c_n\} = 0$. $\blacksquare$

**Definition 2 (Density and Number Operators).** We define the local particle density at site $j$ and the mode occupation number at momentum $n$ as:
$$
n_j = c_j^\dagger c_j, \quad \text{and} \quad n_n = c_n^\dagger c_n
$$
The total particle number operator can be evaluated in either basis: $\hat{N}_{\text{pos}} = \sum_{j} n_j$ and $\hat{N}_{\text{mom}} = \sum_{n} n_n$.

**Theorem 2 (Invariance of the Total Number Operator).** *The total number of fermions is invariant under the basis transformation: $\sum_{j \in \text{Site}_L} n_j = \sum_{n \in \text{Mode}_L} n_n$.*

*Proof.* Expanding the sum of the local densities:
$$
\begin{aligned}
\sum_{j \in \text{Site}_L} n_j &= \sum_{j \in \text{Site}_L} \left( \frac{1}{\sqrt{L}} \sum_{m \in \text{Mode}_L} \zeta^{-mj} c_m^\dagger \right) \left( \frac{1}{\sqrt{L}} \sum_{n \in \text{Mode}_L} \zeta^{nj} c_n \right) \\
&= \sum_{m,n \in \text{Mode}_L} c_m^\dagger c_n \left( \frac{1}{L} \sum_{j \in \text{Site}_L} \zeta^{(n-m)j} \right)
\end{aligned}
$$
Applying the orthogonality property of the roots of unity, the term in parentheses evaluates to $\delta_{m,n}$. Thus:
$$
\sum_{j \in \text{Site}_L} n_j = \sum_{m,n \in \text{Mode}_L} c_m^\dagger c_n \delta_{m,n} = \sum_{n \in \text{Mode}_L} c_n^\dagger c_n = \sum_{n \in \text{Mode}_L} n_n
$$
Therefore, $\hat{N}_{\text{pos}} = \hat{N}_{\text{mom}} \equiv \hat{N}$. $\blacksquare$

***

## Tight-Binding Hamiltonian

The tight-binding model describes fermions hopping between adjacent sites on the lattice. We denote the hopping amplitude by $t$.

**Definition 3 (Standard Tight-Binding Hamiltonian).** 
$$
H = -t \sum_{j \in \text{Site}_L} (c_j^\dagger c_{j+1} + c_{j+1}^\dagger c_j)
$$
*(Note: addition in the subscript is taken modulo $L$, enforcing periodic boundary conditions).*

To cast this into a mathematically revealing form, we introduce discrete difference operators from umbral calculus. Let $I$ be the identity operator, $S$ be the forward shift $(S c)_j = c_{j+1}$, and $S^\dagger$ be the backward shift $(S^\dagger c)_j = c_{j-1}$. 

**Definition 4 (Umbral Difference Operators).** We define the left difference operator $\Delta$ and the right difference operator $\nabla$ acting on the sequence of operators $c$ as:
$$
(\Delta c)_j = c_j - c_{j+1} \\
(\nabla c)_j = c_j - c_{j-1}
$$

**Theorem 3 (Umbral Representation of the Hamiltonian).** *The tight-binding Hamiltonian can be exactly rewritten using the umbral operators as:*
$$
H = t \sum_{j \in \text{Site}_L} c_j^\dagger \big((\Delta + \nabla) c\big)_j - 2t \hat{N}
$$

*Proof.* First, evaluate the action of $(\Delta + \nabla)$ on $c_j$:
$$
\big((\Delta + \nabla) c\big)_j = (c_j - c_{j+1}) + (c_j - c_{j-1}) = 2c_j - c_{j+1} - c_{j-1}
$$
Substitute this into the proposed expression:
$$
\begin{aligned}
t \sum_{j} c_j^\dagger \big((\Delta + \nabla) c\big)_j - 2t \hat{N} &= t \sum_{j} c_j^\dagger (2c_j - c_{j+1} - c_{j-1}) - 2t \sum_{j} c_j^\dagger c_j \\
&= 2t \sum_j c_j^\dagger c_j - t \sum_j c_j^\dagger c_{j+1} - t \sum_j c_j^\dagger c_{j-1} - 2t \sum_j c_j^\dagger c_j \\
&= -t \sum_j (c_j^\dagger c_{j+1} + c_j^\dagger c_{j-1})
\end{aligned}
$$
By shifting the summation index in the second term ($j \to j+1$), we note that $\sum_j c_j^\dagger c_{j-1} = \sum_j c_{j+1}^\dagger c_j$. Thus:
$$
= -t \sum_j (c_j^\dagger c_{j+1} + c_{j+1}^\dagger c_j) \equiv H
$$
$\blacksquare$

**Theorem 4 (Momentum-Space Diagonalization).** *The Hamiltonian is diagonal in the momentum basis:*
$$
H = \sum_{n \in \text{Mode}_L} \varepsilon(n) c_n^\dagger c_n
$$
*with the strict algebraic dispersion relation:*
$$
\varepsilon(n) = -t (\zeta^n + \zeta^{-n})
$$

*Proof.* We express the position operators in $H$ using the momentum-basis definition:
$$
\begin{aligned}
H &= -t \sum_{j} \left( c_j^\dagger c_{j+1} + c_j^\dagger c_{j-1} \right) \\
&= -t \sum_{j} \left[ \left( \frac{1}{\sqrt{L}} \sum_m \zeta^{-mj} c_m^\dagger \right) \left( \frac{1}{\sqrt{L}} \sum_n \zeta^{n(j+1)} c_n \right) + \left( \frac{1}{\sqrt{L}} \sum_m \zeta^{-mj} c_m^\dagger \right) \left( \frac{1}{\sqrt{L}} \sum_n \zeta^{n(j-1)} c_n \right) \right] \\
&= -t \sum_{m,n} c_m^\dagger c_n (\zeta^n + \zeta^{-n}) \left( \frac{1}{L} \sum_{j} \zeta^{(n-m)j} \right)
\end{aligned}
$$
Applying the orthogonality relation $\frac{1}{L} \sum_j \zeta^{(n-m)j} = \delta_{m,n}$, the sum over $m$ evaluates to:
$$
H = -t \sum_{n} (\zeta^n + \zeta^{-n}) c_n^\dagger c_n
$$
Thus, identifying the coefficient of $c_n^\dagger c_n$ yields the dispersion $\varepsilon(n) = -t(\zeta^n + \zeta^{-n})$. $\blacksquare$

*(Note: In the complex plane, $\zeta^n + \zeta^{-n}$ is formally equivalent to $2 \cos(2\pi n /L)$, yielding the familiar cosine band structure. However, maintaining the algebraic $\zeta$ formalism guarantees structural rigidity for subsequent non-commutative or algebraic generalizations).*

***

## Linearized Dispersion

In many advanced many-body treatments (e.g., bosonization following Miranda §III), the relevant physics is dominated by low-energy excitations near the Fermi points. Rather than working with the full tight-binding Hamiltonian, it is analytically powerful to introduce a linearized branch of chiral fermions. 

To formalize this, we define a "sawtooth" dispersion. By shifting our momentum index such that the Fermi point lies at the origin, and restricting ourselves to an isolated chiral right-moving branch, we linearize the dispersion.

**Definition 5 (Linearized Hamiltonian).** Assuming units where the scaled Fermi velocity parameter $2\pi v / L = 1$, we define the formal free Hamiltonian $H_0$ as:
$$
H_0 = \sum_{n \in \text{Mode}_L} n c_n^\dagger c_n
$$
In this regime, the dispersion is strictly linear, $\varepsilon_{\text{lin}}(n) = n$. This abstract operator forms the foundation of the infinite-mode Dirac sea and the subsequent algebraic bosonization mappings.