Below is a practical roadmap for formalizing 1+1D bosonization in Lean 4, with a multi-agent directive, library inventory, required weakening, and references.

## 1. Directive for a Multi-Agent System (Google Antigravity)

**Mission:** Formalize the finite-dimensional core of 1+1D bosonization in Lean 4, targeting a machine-checked proof of the Coleman duality at the level of operators on a truncated Fock space.

**Primary target (achievable):** For a finite-dimensional single-particle space \(V\), construct the antisymmetric Fock space \(\bigwedge V\), define CAR operators, and prove that a unitary map intertwines these with bosonic vertex operators on a finite-dimensional bosonic Fock space.

**Stretch goal (placeholder):** State the infinite-dimensional isomorphism as a `sorry`-able theorem, documenting exactly which analytical results are assumed.

**Hard constraints:**

- **No `sorry` in the core finite-dimensional construction.** Every definition and theorem in the finite-dimensional layer must be complete. `sorry` is allowed only in the infinite-dimensional lift, with a clear `TODO` comment naming the missing analytical lemma.
- **Use Mathlib's `ExteriorAlgebra` and `GradedAlgebra`.** Do not reinvent exterior powers. Leverage the existing graded structure.
- **Model bounded operators only.** Vertex operators are unbounded; on finite-dimensional spaces they become bounded, so this is consistent. Do not attempt to define unbounded operators on a Hilbert space unless absolutely necessary.
- **Stay in `ℂ`.** All vector spaces are complex. Use `InnerProductSpace ℂ V`.
- **Follow Mathlib naming and style.** Use `snake_case` for definitions, `CamelCase` for structures, and `tactic` blocks for proofs.

**Task breakdown for agents:**

1. **Agent A (Algebraic foundations):** Define `FermionicFockSpace (V : Type*) [AddCommGroup V] [Module ℂ V]` as `ExteriorAlgebra ℂ V`. Define the vacuum as `1` in the exterior algebra. Prove the universal property.
2. **Agent B (CAR operators):** For `f : V`, define `creationOp f : ExteriorAlgebra ℂ V →ₗ[ℂ] ExteriorAlgebra ℂ V` as left multiplication by `f`. Define `annihilationOp f` as the adjoint (using the inner product on the exterior algebra). Prove the CAR:
   \[
   \{a(f), a^*(g)\} = \langle f, g\rangle \cdot \mathrm{id}, \quad \{a(f), a(g)\} = 0.
   \]
3. **Agent C (Bosonic side):** Define a finite-dimensional bosonic Fock space as the symmetric algebra `SymmetricAlgebra ℂ W` for a finite-dimensional `W`. Define vertex operators as exponentials of creation/annihilation operators, truncated to finite dimension. Prove that the commutation relations match the CCR.
4. **Agent D (Duality map):** Construct a linear isometry `U : FermionicFockSpace V ≃ₗᵢ[ℂ] BosonicFockSpace W` such that `U (creationOp f) = (vertexOperator g) ∘ U` for some `g` depending on `f`. Prove that `U` maps the fermionic vacuum to the bosonic vacuum.
5. **Agent E (Infinite-dimensional interface):** State the full bosonization isomorphism as a theorem with `sorry`, and document the needed analytical inputs (completion of the Fock space, Haag's theorem avoidance via GNS, etc.).

**Deliverable:** A Lean 4 project with:

- `FermionicFock.lean` — finite-dimensional fermionic Fock space and CAR.
- `BosonicFock.lean` — finite-dimensional bosonic Fock space and vertex operators.
- `Bosonization.lean` — the finite-dimensional unitary isomorphism theorem, fully proved.
- `InfiniteBosonization.lean` — the infinite-dimensional statement with `sorry`, plus a `README.md` explaining the gaps.

## 2. Existing Libraries That Will Help

| Library / Project | What it provides | Where to find it |
|---|---|---|
| **Mathlib `ExteriorAlgebra`** | Definition of exterior algebra, graded structure, universal property, and basis for finite-dimensional spaces. | `Mathlib.LinearAlgebra.ExteriorAlgebra.Basic` and `.Grading` |
| **Mathlib `CliffordAlgebra`** | Clifford algebra as a quotient of the tensor algebra; useful if you prefer CAR via Clifford relations. | `Mathlib.LinearAlgebra.CliffordAlgebra.Basic` |
| **Mathlib `TensorProduct`** | Inner product on tensor products of Hilbert spaces; needed for \(n\)-particle spaces. | `Mathlib.Analysis.InnerProductSpace.TensorProduct` |
| **Mathlib `VonNeumannAlgebra`** | Abstract and concrete von Neumann algebras, C*-algebra basics, GNS construction support. | `Mathlib.Analysis.VonNeumannAlgebra.Basic` |
| **Physicslib4** | Formalization of Haag–Kastler AQFT axioms, causal structure, GNS construction, local von Neumann algebras. | `github.com/physicslib/physicslib4` |
| **QuantumSystem** | GNS construction, Gelfand–Naimark theorem, von Neumann bicommutant, entropy. | `github.com/kencyke/quantum-system` |
| **OSforGFF** | Formalization of free bosonic QFT via Osterwalder–Schrader axioms; shows how to handle Gaussian measures and distributions. | Douglas et al., arXiv:2603.15770 |
| **pphi2** | Construction of \(\phi^4_2\) Euclidean QFT in Lean 4; demonstrates lattice regularization and continuum limit. | Reservoir entry `pphi2` |

**Key takeaway:** You do not need to build the exterior algebra from scratch. Mathlib's `ExteriorAlgebra` with its graded structure is the correct starting point. For the operator algebra layer, `VonNeumannAlgebra` and the GNS construction from Physicslib/QuantumSystem give you the AQFT scaffolding.

## 3. Adaptations and Weakening You Must Accept

Formalizing the full bosonization isomorphism in Lean 4 is currently infeasible. The following weakenings are necessary to make the project realistic.

### 3.1 Finite-dimensional truncation (mandatory)

**Problem:** The physical Fock space is an infinite direct sum of tensor powers, completed in norm. Mathlib's `ExteriorAlgebra` gives the algebraic direct sum, which is *not* complete.

**Weakening:** Work with a finite-dimensional single-particle space \(V\) (e.g., \(V = \mathbb{C}^N\) with \(N\) a finite mode cutoff). Then \(\bigwedge V\) is finite-dimensional and automatically complete. All operators are bounded. The CAR and CCR hold exactly.

**Why this is honest:** Finite-dimensional Fock spaces are used in lattice regularization of QFT. The physical limit is recovered by taking \(N \to \infty\), but the finite-\(N\) structure is mathematically rigorous and machine-checkable.

### 3.2 Bounded vertex operators only

**Problem:** The vertex operator \(:\exp(i\sqrt{4\pi}\phi):\) is unbounded on the infinite-dimensional bosonic Fock space.

**Weakening:** On a finite-dimensional bosonic Fock space, the exponential of a bounded operator is bounded. Define the vertex operator as a finite sum (truncated exponential) and prove that it satisfies the required intertwining property. The infinite-dimensional unbounded case is left as `sorry`.

### 3.3 No Haag's theorem avoidance

**Problem:** Haag's theorem states that the free and interacting Fock spaces are unitarily inequivalent in infinite volume. Bosonization is an exact equivalence, so it avoids this issue, but proving the equivalence requires the GNS construction with a specific vacuum state.

**Weakening:** In the finite-dimensional setting, there is no infinite-volume limit, so Haag's theorem does not apply. State the GNS-based infinite-dimensional construction as a `sorry`-able theorem with a clear explanation of the missing analytical input.

### 3.4 No distributional fields

**Problem:** In the Wightman framework, fields are operator-valued distributions. Passing a point \(x\) to \(\phi\) is not defined.

**Weakening:** In the finite-dimensional setting, use smeared fields \(\phi(f)\) where \(f\) is a test function, but discretize the test function space to a finite-dimensional subspace. This matches the lattice regularization approach.

### 3.5 Operator algebra: use concrete bounded operators

**Problem:** The CAR algebra is a C*-algebra generated by unbounded field operators. Mathlib's `VonNeumannAlgebra` is designed for bounded operators.

**Weakening:** Represent the CAR algebra as a subalgebra of bounded operators on the finite-dimensional Fock space. This is a faithful representation of the algebraic CAR relations. Prove the CAR as an algebraic identity in `End(ℂ, ⋀ V)`.

### 3.6 Lattice regularization instead of continuum

**Problem:** The continuum bosonization formula involves distributions, normal ordering, and UV cutoffs.

**Weakening:** Formulate bosonization on a finite lattice (e.g., a periodic chain of length \(N\)). The fermionic and bosonic Fock spaces are finite-dimensional. The bosonization map becomes a finite-dimensional unitary matrix. The continuum limit is a separate, non-formalized step.

## 4. References

- **Mathlib Exterior Algebra:** `Mathlib.LinearAlgebra.ExteriorAlgebra.Basic`, `Mathlib.LinearAlgebra.ExteriorAlgebra.Grading`
- **Mathlib Clifford Algebra:** `Mathlib.LinearAlgebra.CliffordAlgebra.Basic`
- **Mathlib Tensor Product of Hilbert Spaces:** `Mathlib.Analysis.InnerProductSpace.TensorProduct`
- **Mathlib Von Neumann Algebras:** `Mathlib.Analysis.VonNeumannAlgebra.Basic`
- **Physicslib4 (AQFT):** `github.com/physicslib/physicslib4`
- **QuantumSystem (GNS, Gelfand–Naimark):** `github.com/kencyke/quantum-system`
- **Douglas et al., “Formalization of QFT” (OS axioms for free field):** arXiv:2603.15770
- **Coleman, “Quantum Sine-Gordon Equation as the Massive Thirring Model” (1975):** The original duality paper.
- **Mandelstam, “Soliton Operators for the Quantized Sine-Gordon Equation” (1975):** The vertex operator construction.
- **Haag–Kastler axioms:** Haag, R., & Kastler, D. (1964). *J. Math. Phys.*, 5(7), 848–861.
- **Glimm & Jaffe, *Quantum Physics: A Functional Integral Point of View*:** Standard reference for constructive QFT and lattice regularization.

## Summary

The realistic path is: **finite-dimensional algebraic Fock spaces → CAR/CCR operators → finite-dimensional unitary bosonization map → `sorry`-able infinite-dimensional lift.** This yields a machine-checked proof of the *algebraic core* of bosonization, with a clear formal interface to the analytical completion. The multi-agent directive above assigns concrete, verifiable tasks to each agent, leveraging Mathlib's `ExteriorAlgebra`, `CliffordAlgebra`, and `VonNeumannAlgebra` libraries. The weakenings are not compromises of mathematical honesty—they are the standard finite-dimensional approximations used in constructive QFT, now made rigorous in Lean.




---


In formal algebraic quantum field theory (AQFT) and constructive field theory, the Hilbert space for a 1+1 dimensional free Majorana or Dirac fermion is constructed by completing the Fock space over a specific one-particle Hilbert space, which is determined by the solutions of the Dirac equation.
Here is how the Hilbert/Fock space is formally defined.
## 1. The One-Particle Hilbert Space $\mathcal{H}_1$
Before constructing the many-body Fock space, we must define the single-particle states. We start with the classical 1+1 dimensional Dirac equation for a mass $m \geq 0$:
$$(i\gamma^\mu \partial_\mu - m)\psi(x) = 0$$
where $x = (x^0, x^1) \in \mathbb{R}^{1+1}$, and $\gamma^\mu$ are $2 \times 2$ Dirac matrices satisfying $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}$.

* Solution Space: Let $\mathcal{S}$ be the space of smooth, compact-support (or rapidly decreasing) test spinors.
* Inner Product: We define a positive-definite inner product on the space of positive-energy solutions. By Fourier transforming the solutions to momentum space, the mass shell is the hyperbola $k^2 = (k^0)^2 - (k^1)^2 = m^2$.
* For a Majorana fermion (where $\psi$ is a self-conjugate real spinor), the one-particle Hilbert space $\mathcal{H}_1$ is the completion of the positive-energy solution space under the Lorentz-invariant inner product:
$$\langle f, g \rangle_{\mathcal{H}_1} = \int_{-\mathbb{R}} \frac{dk^1}{2\omega_k} \bar{u}(k)f(k) v(k)g(k)$$
where $\omega_k = \sqrt{(k^1)^2 + m^2}$.

## 2. The Antisymmetric Fock Space $\mathcal{F}_a(\mathcal{H}_1)$
Because fermions obey the Pauli exclusion principle, the total Hilbert space $\mathcal{H}$ is the antisymmetric Fock space generated by $\mathcal{H}_1$. It is defined as the direct sum of $n$-particle antisymmetric Hilbert spaces:
$$\mathcal{H} = \mathcal{F}_a(\mathcal{H}_1) = \bigoplus_{n=0}^{\infty} \bigwedge^n \mathcal{H}_1$$
Where:

* $\bigwedge^0 \mathcal{H}_1 \cong \mathbb{C}$ is the 1-dimensional subspace spanned by the vacuum state $\vert{}\Omega\rangle$.
* $\bigwedge^1 \mathcal{H}_1 = \mathcal{H}_1$ is the single-particle space.
* $\bigwedge^n \mathcal{H}_1$ is the closed subspace of the $n$-fold tensor product $\mathcal{H}_1^{\otimes n}$ spanned by totally antisymmetric vectors:
$$\psi_1 \wedge \psi_2 \wedge \dots \wedge \psi_n = \frac{1}{\sqrt{n!}} \sum_{\sigma \in S_n} \text{sgn}(\sigma) \psi_{\sigma(1)} \otimes \dots \otimes \psi_{\sigma(n)}$$

## 3. Connection to AQFT (The CAR Algebra)
In the algebraic framework, rather than starting with the Hilbert space, one often starts with the Canonical Anticommutation Relations (CAR) algebra, denoted as $\mathcal{A}(\mathcal{H}_1)$.

* For every element $f \in \mathcal{H}_1$, there exist bounded linear operators $a(f)$ and $a^*(f)$ acting on $\mathcal{F}_a(\mathcal{H}_1)$ satisfying:
$$\{a(f), a^*(g)\} = \langle f, g \rangle_{\mathcal{H}_1} I$$
$$\{a(f), a(g)\} = 0, \quad \{a^*(f), a^*(g)\} = 0$$
* Fock Representation: The standard Hilbert space $\mathcal{H}$ is recovered via the GNS (Gelfand-Naimark-Segal) construction applied to the CAR algebra using the unique vacuum state $\omega_0$ (a pure, vacuum state uniquely invariant under the lifted Poincaré representations), such that $a(f)\vert{}\Omega\rangle = 0$ for all $f$.

## 4. Special Features in 1+1 Dimensions
When working specifically in 1+1 dimensions, two unique simplifications occur:

* Light-Cone Decoupling: For massless fermions ($m=0$), the Dirac equation completely decouples into independent left-moving (chiral) and right-moving (anti-chiral) components. The one-particle space factors as $\mathcal{H}_1 = \mathcal{H}_L \oplus \mathcal{H}_R$, and the total Fock space factors tensorially: $\mathcal{F}_a(\mathcal{H}_1) \cong \mathcal{F}_a(\mathcal{H}_L) \otimes \mathcal{F}_a(\mathcal{H}_R)$.
* Bosonization: Due to the simple topology of the 1+1 mass shell (which disconnects into left/right branches), the fermionic Fock space $\mathcal{F}_a(\mathcal{H}_1)$ is unitarily isomorphic to a bosonic Fock space $\mathcal{F}_s(\mathcal{H}_{\text{boson}})$. This allows formal representations of fermionic operators using vertex operators of a scalar free field.


In $1+1$ dimensions, bosonization is an exact equivalence between a theory of Dirac fermions and a theory of a compact scalar boson. At the level of operators, this duality maps the non-local fermionic fields to local vertex operators of the bosonized scalar field.
Here is how the formula is formally expressed for a free fermion and its structural dualities.
------------------------------
## 1. The Chiral Bosonization Dictionary
For a massless free Dirac fermion $\psi$, we decompose the spinor into its left-moving (chiral) and right-moving (anti-chiral) components:
$$\psi(x) = \begin{pmatrix} \psi_L(x^0 - x^1) \\ \psi_R(x^0 + x^1) \end{pmatrix}$$
The bosonization formula maps these independent Weyl fermions to a single, real-valued free scalar field $\phi(x^0, x^1)$. The explicit relation for the fermionic fields is given by the vertex operator formula:
$$\psi_L(x) = \frac{1}{\sqrt{2\pi a}} :\exp\left( -i \sqrt{4\pi} \phi_L(x) \right):$$
$$\psi_R(x) = \frac{1}{\sqrt{2\pi a}} :\exp\left( i \sqrt{4\pi} \phi_R(x) \right):$$
Where:

*
* $a$ is a short-distance UV regularization cutoff.
* $:\dots:$ denotes normal ordering with respect to the vacuum.
* $\phi_L$ and $\phi_R$ are the left- and right-moving chiral components of the scalar field $\phi = \phi_L + \phi_R$.
*

------------------------------
## 2. The Current Duality (Bosonization Dictionary)
The deep structural duality between the two systems translates gauge currents into topological gradients. If you look at the conserved currents on both sides, they match exactly via the following equations:

| Fermionic Operator | Bosonized Operator Equivalent | Description |
|---|---|---|
| Vector Current: $j^\mu = :\bar{\psi} \gamma^\mu \psi:$ | $j^\mu = \frac{1}{\sqrt{\pi}} \epsilon^{\mu\nu} \partial_\nu \phi$ | The $U(1)$ fermion current maps to the topological current of the boson. |
| Axial Current: $j_A^\mu = :\bar{\psi} \gamma^\mu \gamma^5 \psi:$ | $j_A^\mu = \frac{1}{\sqrt{\pi}} \partial^\mu \phi$ | The chiral current maps to the canonical momentum gradient. |
| Mass Term: $\bar{\psi}\psi = \psi_L^\dagger \psi_R + \psi_R^\dagger \psi_L$ | $-\frac{\mathcal{C}}{\pi a} \cos\left(\sqrt{4\pi}\phi\right)$ | The fermion mass bilinear translates into a cosine potential ($\mathcal{C}$ is a constant). |

------------------------------
## 3. Generalization to Dualities: The Massive Case
When a mass term $m\bar{\psi}\psi$ is added to the free fermion, it triggers a famous field-theoretic duality known as Coleman's Duality (or the Massive Thirring / Sine-Gordon duality).
If we generalize the free fermion to include a four-fermion interaction (the Massive Thirring Model), it maps perfectly to the Sine-Gordon model for a self-interacting scalar boson:
$$\mathcal{L}_{\text{Thirring}} = i\bar{\psi}\gamma^\mu\partial_\mu\psi - m\bar{\psi}\psi - \frac{g}{2}(j^\mu j_\mu) \quad \longleftrightarrow \quad \mathcal{L}_{\text{Sine-Gordon}} = \frac{1}{2}(\partial_\mu\phi)^2 + \frac{\alpha_0}{\beta^2}\cos(\beta\phi)$$
The exact duality map between the coupling constants is given by:
$$\frac{\beta^2}{4\pi} = \frac{1}{1 + g/\pi}$$

*
* The Free Fermion Point ($g=0$): This corresponds precisely to $\beta = \sqrt{4\pi}$, reducing the Sine-Gordon model to a free massive boson theory.
* Strong-Weak Duality: When the fermion interaction is strongly attractive or repulsive, it maps to a weakly coupled scalar field, making bosonization a highly effective tool for analyzing non-perturbative regimes.
*


 To formalize the free fermion and bosonization in Lean 4, you need to translate the algebraic concepts—the Canonical Anticommutation Relations (CAR) algebra and the Canonical Commutation Relations (CCR) algebra—into type-theoretic structures.
In formal constructive field theory, the starting point is proving that a map from a single-particle Hilbert space into a bounded operator algebra satisfies the CAR. The ultimate goal of bosonization is proving a unitary isomorphism between the fermionic Fock space and the bosonic Fock space that preserves these algebraic structures.
Here is how you can set up a formal Lean 4 template for the starting point and the ultimate goal.
------------------------------
## 1. The Starting Point: Defining the CAR Algebra
First, we must define what it means for a set of operators to satisfy the CAR over a real or complex inner product space (the single-particle space $\mathcal{H}_1$).

import Mathlib.Analysis.InnerProductSpace.Basicimport Mathlib.Algebra.Algebra.Basic
open InnerProductSpace
-- Let H1 be a complex Hilbert space representing the single-particle statesvariable (H1 : Type*) [NormedAddCommGroup H1] [InnerProductSpace ℂ H1] [CompleteSpace H1]
/-- The Starting Point: Define the Canonical Anticommutation Relations (CAR)
    as a property of a linear map from H1 to a bounded operator algebra. -/structure IsCarAlgebra (A : Type*) [Ring A] [Algebra ℂ A] (a : H1 →ₗ[ℂ] A) : Prop :=
(anticomm_creation : ∀ f g : H1, a f * a g + a g * a f = 0)
(anticomm_annihilation : ∀ f g : H1, (a f) * (a g) + (a g) * (a f) = 0) -- usually modeled via star-algebra
(car_relation : ∀ f g : H1, a f * (a g) + (a g) * a f = inner f g • (1 : A)) -- structural definition

(Note: A highly rigorous approach often uses CliffordAlgebra over a quadratic form derived from the inner product, as Lean's Mathlib already has a robust Clifford Algebra library.)
------------------------------
## 2. The Intermediate Structure: The Fermionic Fock Space
We define the antisymmetric Fock space as an infinite direct sum of alternating tensor powers.

-- Representing the abstract Fock Space as a Typeaxiom FermionicFockSpace (H1 : Type*) [InnerProductSpace ℂ H1] : Type*
-- The vacuum vector in the Fock spaceaxiom vacuumState {H1 : Type*} [InnerProductSpace ℂ H1] : FermionicFockSpace H1
-- The creation/annihilation operators acting on the Fock Spaceaxiom creationOp {H1 : Type*} [InnerProductSpace ℂ H1] (f : H1) :
  FermionicFockSpace H1 →ₗ[ℂ] FermionicFockSpace H1

------------------------------
## 3. The Ultimate Goal: The Bosonization Isomorphism
The goal of bosonization is to state that there exists a unitary equivalence ($\simeq_{U}$) between the Fermionic Fock space of the 1+1D Dirac field and the Bosonic Fock space of a scalar field, such that the vacuum maps to the vacuum, and the vertex operators match the fermion operators.
Here is how that theorem statement looks in Lean 4 syntax:

-- Assume similar definitions exist for the Bosonic Fock Spaceaxiom BosonicFockSpace (H_boson : Type*) [InnerProductSpace ℂ H_boson] : Type*axiom bosonicVacuum {H_boson : Type*} [InnerProductSpace ℂ H_boson] : BosonicFockSpace H_boson
-- A vertex operator parameterized by a bosonic test functionaxiom vertexOperator {H_boson : Type*} [InnerProductSpace ℂ H_boson] (g : H_boson) :
  BosonicFockSpace H_boson →ₗ[ℂ] BosonicFockSpace H_boson
/-- The Goal: The Bosonization Equivalence Theorem -/theorem bosonization_isomorphism
  (H_fermion : Type*) [InnerProductSpace ℂ H_fermion] [CompleteSpace H_fermion]
  (H_boson : Type*) [InnerProductSpace ℂ H_boson] [CompleteSpace H_boson] :
  Exists (fun (U : FermionicFockSpace H_fermion ≃ₗᵢ[ℂ] BosonicFockSpace H_boson) =>
    -- 1. It maps the fermionic vacuum to the bosonic vacuum
    U vacuumState = bosonicVacuum ∧
    -- 2. It intertwines the fermion operators with the bosonic vertex operators
    ∀ (f : H_fermion), ∃ (g : H_boson),
      U ∘ (creationOp f) = (vertexOperator g) ∘ U
  ) := by
  sorry

## Why this is a challenging project in Lean 4

   1. Infinite-dimensional Tensor Products: Mathlib easily handles finite exterior algebras (ExteriorAlgebra), but completing the infinite direct sum of anti-symmetrized tensor products to build $\mathcal{F}_a(\mathcal{H}_1)$ requires deep analytical machinery.
   2. Unbounded Operators / Distributional Vertex Operators: Rigorous AQFT deals with distributions. In Lean, you would either need to define vertex operators via a UV cutoff (as bounded operators on a lattice or a cylinder) or map them as elements of a continuous linear map topology.






## 1. Finite-Dimensional Exterior Algebra in Lean 4
In Lean 4's mathematical library (Mathlib), the exterior algebra $\bigwedge V$ over a module or vector space $V$ is defined via a universal property as a quotient of the tensor algebra.
For a finite-dimensional vector space, you can define the space and its graded components. Here is how you state the finite-dimensional exterior algebra and its algebraic grading in Lean 4:

import Mathlib.LinearAlgebra.ExteriorAlgebra.Basicimport Mathlib.LinearAlgebra.ExteriorAlgebra.Grading
open ExteriorAlgebra
-- Let V be a finite-dimensional complex vector spacevariable (V : Type*) [AddCommGroup V] [Module ℂ V] [FiniteDimensional ℂ V]
/-- The total exterior algebra over V -/def FiniteExteriorAlgebra := ExteriorAlgebra ℂ V
/-- The n-th exterior power of V (the n-th graded component) -/def ExteriorPower (n : ℕ) := Grading.gradedComponent ℂ V n

------------------------------
## 2. Why Can't We Just Take the Inductive Limit + UV Regulator?
Physicists often construct infinite-dimensional spaces by introducing a UV regulator (like putting the system on a lattice of size $N$ or using a momentum cutoff $\Lambda$), defining a finite-dimensional space $\mathcal{H}_N$, and taking the limit $N \to \infty$.
In formal mathematics and Lean, this approach fails to yield the correct Hilbert space due to structural and topological obstructions:
## I. The Inductive Limit in Topologies (The Complete Space Problem)
In category theory and algebra, you can easily take the inductive limit (direct limit) of vector spaces:
$$\mathcal{H}_{\infty, \text{alg}} = \lim_{\longrightarrow} \mathcal{H}_N$$
However, this yields a purely algebraic direct limit.

* The issue: The algebraic direct limit of an infinite sequence of expanding Hilbert spaces is never complete. It contains only vectors that have a finite number of non-zero particle components or live entirely within some finite-dimensional subspace $N$.
* The fix: You must take the topological completion of this limit space. In Lean, you cannot just say lim; you must explicitly invoke the Cauchy completion (CompleteSpace) under the specified Hilbert norm.

## II. Haag's Theorem and Inequivalent Representations
The core obstacle in rigorous AQFT is Haag's Theorem, which states that the interaction picture does not exist in an infinite-dimensional quantum field theory.

* When you remove a UV cutoff ($N \to \infty$), the infinite-dimensional Fock space you build for a free theory is unitarily inequivalent to the space of a interacting theory.
* A simple inductive limit implies there is a single, universal "large box" space containing all states. In reality, the limit depends entirely on the chosen vacuum state. If you change parameters (like the mass $m$ or a coupling constant $g$), the limit spaces become completely orthogonal to each other in the infinite volume limit.

## III. Constructive vs. Non-Constructive Limits
In Lean, defining a limit requires proving that the transition maps between $\mathcal{H}_N$ and $\mathcal{H}_{N+1}$ are isometries (preserving the inner product).

* For a free fermion, as you scale the UV cutoff $N$, the embedding map $\iota_N: \mathcal{H}_N \to \mathcal{H}_{N+1}$ depends on how you regularize. If the inner product changes with $N$ (due to wavefunction renormalization constants $Z_N$ which typically diverge as $N \to \infty$), the maps are not isometric.
* Lean will reject a naive limit because the sequence of spaces does not form a valid directed system under a constant metric.

## The Formal Solution
Instead of taking a limit of spaces, AQFT solves this by separating the algebra from the state:

   1. You construct the inductive limit of the CAR Algebras $\mathcal{A}_N$ (which forms a well-behaved $C^*$-algebra $\mathcal{A}_\infty$).
   2. You define a vacuum state $\omega$ as a linear functional on $\mathcal{A}_\infty$.
   3. You perform the GNS Construction, which outputs the correct, completed Hilbert space $\mathcal{H}_\omega$ unique to that specific vacuum.




In Lean 4, formalizing Algebraic Quantum Field Theory (AQFT) or Wightman axioms requires moving away from casual physics notations and treating spacetime regions, operator algebras, and distributions as clean mathematical types.
For the 1+1 dimensional case, things simplify dramatically because the causal structure is explicitly dictated by light-cones, and the spacetime is simply $\mathbb{R}^{1+1}$.
Here is how both frameworks—AQFT (Local Von Neumann/C*-Algebras) and Wightman Axioms (Distributions)—are typically framed as objects in Lean 4.
------------------------------
## 1. Framing AQFT / Local Algebras in Lean 4
In AQFT (the Haag-Kastler framework), you do not look at point-like fields. Instead, you assign a algebra of observables $\mathcal{A}(\mathcal{O})$ to every bounded open region $\mathcal{O}$ in spacetime.
To set this up in Lean 4, we define a poset mapping from open sets of 1+1D Minkowski space to sub-C*-algebras of a global algebra (or bounded operators on a Hilbert space).

import Mathlib.Topology.Basicimport Mathlib.Analysis.InnerProductSpace.Adjointimport Mathlib.Algebra.Category.ModuleCat.Basic
open TopologicalSpace
-- 1. Define 1+1 Minkowski Space as a vector space with a custom metricstructure Minkowski2 :=
  (t : ℝ) (x : ℝ)
-- Define the causal separation condition for 1+1 Dimensionsdef spaceLike (p1 p2 : Minkowski2) : Prop :=
  (p1.t - p2.t)^2 < (p1.x - p2.x)^2
-- Let H be the global Hilbert space of the theoryvariable (H : Type*) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
-- A local algebra can be modeled as a subalgebra of bounded linear operators
abbrev BoundedOps := H →L[ℂ] H
/-- The Haag-Kastler Axioms for 1+1D AQFT -/structure AQFT2D :=
  -- A net that assigns a set of bounded operators to open regions in Minkowski space
  (net : TopologicalSpace.Opens Minkowski2 → Subalgebra ℂ BoundedOps)

  -- Isotony: If O1 ⊆ O2, then A(O1) ⊆ A(O2)
  (isotony : ∀ (O1 O2 : TopologicalSpace.Opens Minkowski2), O1 ≤ O2 → net O1 ≤ net O2)

  -- Microcausality: Space-like separated regions commute
  (microcausality : ∀ (O1 O2 : TopologicalSpace.Opens Minkowski2),
    (∀ (p1 ∈ O1) (p2 ∈ O2), spaceLike p1 p2) →
    ∀ (A ∈ net O1) (B ∈ net O2), A * B = B * A)

------------------------------
## 2. Framing Wightman Axioms in Lean 4
The Wightman framework focuses on point-like field operators $\phi(x)$, which mathematically are operator-valued distributions. In Lean, you cannot pass a point $x \in \mathbb{R}^2$ directly to $\phi$; you must feed it a smooth, compactly supported test function $f \in \mathcal{C}_c^\infty(\mathbb{R}^2)$.
To declare this in Lean 4, we use the vector space of test functions to index our operators.

-- Representing the space of smooth, compactly supported test functions on ℝ²-- (In complete formalizations, this uses the topological vector space structure of D(ℝ²))axiom TestFunctions2D : Type*axiom TestFunctions2D.is_space_like_sep (f g : TestFunctions2D) : Prop
/-- A simplified setup for 2D Wightman fields -/structure WightmanField2D (H : Type*) [InnerProductSpace ℂ H] [CompleteSpace H] :=
  -- The field is a linear map from test functions to (potentially unbounded) operators
  -- For simplicity here, we assume a domain D invariant under the fields
  (D : Subspace ℂ H)
  (phi : TestFunctions2D →ₗ[ℂ] (D →ₗ[ℂ] D))

  -- Axiom of Locality (Causality)
  (locality : ∀ (f g : TestFunctions2D), TestFunctions2D.is_space_like_sep f g →
    ∀ (v : D), phi f (phi g v) = phi g (phi f v))

------------------------------
## Why 1+1 Dimensions is Structurally Unique in Lean 4
When implementing the 1+1D case explicitly, you gain geometric properties that make your Lean proofs significantly easier compared to 3+1D:

   1. Light-Cone Coordinates: You can redefine your spacetime coordinates from $(t, x)$ to light-cone variables $u = t - x$ and $v = t + x$. Under this transformation, the spacetime splits into a product of two independent 1D manifolds: $\mathbb{R}^{1+1} \cong \mathbb{R}_L \times \mathbb{R}_R$.
   2. Interval Posets: Bounded causal regions (known as double cones) can be parameterized simply as a pair of open intervals $(a, b) \times (c, d)$ in light-cone space. Instead of using generalized topology libraries, your net can be indexed by a simple type: (Real × Real) × (Real × Real), making the proofs for Isotony and Microcausality pure arithmetic inequality checks.
