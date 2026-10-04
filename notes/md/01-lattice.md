***

# Lattice, Band, and Index Types

In 1+1-dimensional lattice quantum field theory, particularly in the study of bosonization and dualities such as QED$_3$, the exact specification of the discrete spatial manifold and its Fourier-dual momentum space is foundational. To define the Canonical Anticommutation Relations (CAR) algebra and the corresponding fermionic Fock space without ambiguity, we must carefully define the spatial lattice, the momentum band (Brillouin zone), and the internal degrees of freedom (such as chirality). 

This section rigorously defines these structures and establishes the canonical bijections that govern the discrete Fourier transform. Throughout this section, let $L \in \mathbb{N}^+$ denote the number of spatial lattice sites.

## Definitions

**Definition 1 (Spatial Lattice).** 
The 1D spatial lattice is defined as a periodic ring of $L$ sites. Mathematically, we identify the lattice with the additive group of integers modulo $L$, denoted by $\mathbb{Z}_L$. We refer to the set of spatial positions as the **Site** space, defined as:
$$ \text{Site}_L := \mathbb{Z}/L\mathbb{Z} \cong \mathbb{Z}_L $$
Points $x \in \text{Site}_L$ inherently respect periodic boundary conditions, as addition is naturally evaluated modulo $L$.

**Definition 2 (Momentum Band).** 
To accommodate the discrete Fourier transform, the momentum space (or Brillouin zone) must be a dual lattice. To properly treat physical phenomena like the Fermi sea and chiral anomalies, it is heavily advantageous to define a *centered* momentum band rather than an arbitrary fundamental domain of $\mathbb{Z}_L$. 

We define the centered momentum band, referred to as the **Mode** space, as the subset of integers $n \in \mathbb{Z}$ that satisfy the boundary constraints $-L < 2n \le L$. Formally:
$$ \text{Mode}_L := \left\{ n \in \mathbb{Z} \ \Big|\ -L < 2n \le L \right\} $$
Equivalently, this is the set of integers falling in the half-open interval $(-\frac{L}{2}, \frac{L}{2}]$.

**Definition 3 (Chirality).** 
In 1+1D Dirac/Majorana theories, the continuous Lorentz group $SO(1,1)$ leads to spinors decomposing into right-moving and left-moving Weyl components. On the lattice, we preserve this index to define staggered or Wilson fermions. We define the **Chirality** index space as a finite set of two elements:
$$ \mathcal{C} := \{ R, L \} \cong \{ +1, -1 \} $$

**Definition 4 (Single-Particle Index Type).** 
To construct the fermionic Fock space, we require a composite index that labels the single-particle creation and annihilation operators. The total **Index** type for a momentum-space fermion is defined as the Cartesian product of the Chirality and the Mode space:
$$ \text{Index}_L := \mathcal{C} \times \text{Mode}_L $$
A single-particle state is thus uniquely specified by a tuple $(\nu, n)$, where $\nu \in \mathcal{C}$ and $n \in \text{Mode}_L$. This index type forms the indexing set for the CAR algebra generators, $c^\dagger_{\nu, n}$ and $c_{\nu, n}$.

---

## Theorems

To ensure that the discrete Fourier transform between position space and momentum space is a well-defined isomorphism, we must prove that the centered momentum band has exactly $L$ states and is canonically isomorphic to the spatial lattice.

**Theorem 1 (Cardinality of the Momentum Band).** 
*For any positive integer $L$, the cardinality of the momentum band $\text{Mode}_L$ is exactly $L$.*

*Proof.* 
By definition, $n \in \text{Mode}_L$ if and only if $n \in \mathbb{Z}$ and $-L < 2n \le L$. Dividing the inequalities by 2 yields:
$$ -\frac{L}{2} < n \le \frac{L}{2} $$
Because $n$ must be an integer, we can express these bounds using the floor and ceiling functions:
$$ \lfloor -L/2 \rfloor + 1 \le n \le \lfloor L/2 \rfloor $$
It is a standard property of the integers that the number of integers in a half-open interval $(a, b]$ of length $b-a = L$ is exactly $L$. Therefore, the number of valid modes $n$ is identically $L$. $\blacksquare$

**Theorem 2 (Canonical Bijection between Band and Lattice).** 
*There exists a canonical bijection $\phi : \text{Mode}_L \to \text{Site}_L$ that preserves the periodic boundary conditions of the lattice.*

*Proof.* 
Define the canonical projection map $\phi : \mathbb{Z} \to \mathbb{Z}_L$ by taking the equivalence class modulo $L$:
$$ \phi(n) = n \pmod L $$
We restrict $\phi$ to the domain $\text{Mode}_L$. To show $\phi|_{\text{Mode}_L}$ is a bijection, we note that by Theorem 1, $|\text{Mode}_L| = |\mathbb{Z}_L| = L$. For finite sets of equal cardinality, it suffices to prove injectivity.

Assume there exist $n, m \in \text{Mode}_L$ such that $\phi(n) = \phi(m)$. This implies that $n \equiv m \pmod L$, or equivalently, that $n - m = kL$ for some $k \in \mathbb{Z}$.
Because $n, m \in \text{Mode}_L$, they both satisfy $-\frac{L}{2} < n, m \le \frac{L}{2}$. 
The maximum possible difference between any two elements in this interval strictly bounded by:
$$ -\left(\frac{L}{2} - \left(-\frac{L}{2}\right)\right) < n - m < \left(\frac{L}{2} - \left(-\frac{L}{2}\right)\right) $$
$$ -L < n - m < L $$
The only integer multiple of $L$ that lies strictly between $-L$ and $L$ is $0$. Thus, $n - m = 0$, which implies $n = m$. 
Therefore, $\phi$ is injective, and consequently bijective. This establishes the equivalence $\text{Mode}_L \cong \text{Site}_L$, ensuring that momentum operations modulo $L$ canonically map back to identical physical lattice states. $\blacksquare$

---

## Lean Implementation

The mathematical structures defined above translate directly into the Lean 4 formalization of the lattice QFT. The rigorous typing of Lean ensures that boundary conditions and band dimensionalities are checked at compile time.

**1. Lattice Space (`Site L`)**
The spatial lattice is implemented directly as the cyclic group `ZMod L`, automatically inheriting modulo arithmetic.
```lean
def Site (L : ℕ) := ZMod L
```

**2. Momentum Band (`Mode L`)**
The momentum band is implemented as a Subtype of the integers (`ℤ`), constrained by the inequalities defined in Definition 2. 
```lean
def Mode (L : ℕ) := { n : ℤ // -L < 2 * n ∧ 2 * n ≤ L }
```
*Note: In Lean, `L` is implicitly cast to `ℤ` within the inequalities.*

**3. Equivalence / Bijection**
Theorem 2 is implemented as an `Equiv` (a bundled bijection) in Lean. This allows seamless transitions between momentum indices and spatial indices.
```lean
def modeEquivSite {L : ℕ} [NeZero L] : Mode L ≃ Site L :=
  -- Implementation relies on `ZMod.cast` and proving injectivity 
  -- via bounds analysis, mirroring Theorem 2.
```

**4. Chirality and Index**
The two-component nature of the fermions is implemented via an inductive type, and the fundamental index type for the CAR algebra operators is their Cartesian product.
```lean
inductive Chirality
  | R
  | L
deriving DecidableEq, Repr, Fintype

def Index (L : ℕ) := Chirality × Mode L
```
By composing `Fintype` instances, Lean automatically infers that `Index L` has cardinality $2L$, accurately reflecting the degrees of freedom of a single Dirac fermion living on an $L$-site spatial lattice.