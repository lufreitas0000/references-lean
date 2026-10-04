# Mathlib Audit

This document contains an audit of the Mathlib names required for Phase 1 of the BOSONIZE-LEAN project.

| Area | Name | Status | Actual name / signature (abridged) | Module |
|---|---|---|---|---|
| Number Theory | ZMod | FOUND | `ZMod : ℕ → Type` | `Mathlib.Data.ZMod.Basic` |
| Number Theory | ZMod.val | FOUND | `ZMod.val {n : ℕ} : ZMod n → ℕ` | `Mathlib.Data.ZMod.Basic` |
| Number Theory | ZMod.natCast_self | FOUND | `ZMod.natCast_self (n : ℕ) : ↑n = 0` | `Mathlib.Data.ZMod.Basic` |
| Number Theory | ZMod.intCast_cast | FOUND | `ZMod.intCast_cast : ↑i.cast = i.cast` | `Mathlib.Data.ZMod.Basic` |
| Finite Diff | fwdDiff | FOUND | `fwdDiff (h : M) (f : M → G) : M → G` | `Mathlib.Algebra.Group.ForwardDiff` |
| Finite Diff | fwdDiff_iter_eq_sum_shift | FOUND | `fwdDiff_iter_eq_sum_shift : (fwdDiff h)^[n] f y = ∑ k, ...` | `Mathlib.Algebra.Group.ForwardDiff` |
| Polynomials | descPochhammer | FOUND | `descPochhammer : ℕ → Polynomial R` | `Mathlib.RingTheory.Polynomial.Pochhammer` |
| Polynomials | ascPochhammer | FOUND | `ascPochhammer : ℕ → Polynomial S` | `Mathlib.RingTheory.Polynomial.Pochhammer` |
| Polynomials | Polynomial.derivative | FOUND | `Polynomial.derivative : Polynomial R →ₗ[R] Polynomial R` | `Mathlib.Data.Polynomial.Derivative` |
| Polynomials | Polynomial.comp | FOUND | `Polynomial.comp : Polynomial R → Polynomial R → Polynomial R` | `Mathlib.Data.Polynomial.Eval` |
| Polynomials | Polynomial.taylor | FOUND | `Polynomial.taylor (r : R) : Polynomial R →ₗ[R] Polynomial R` | `Mathlib.Data.Polynomial.Taylor` |
| Big Operators | Finset.sum_range_succ_sub_sum | FOUND | `Finset.sum_range_succ_sub_sum : ∑ i ∈ range (n + 1), f i - ∑ i ∈ range n, f i = f n` | `Mathlib.Algebra.BigOperators.Intervals` |
| Big Operators | Finset.sum_range_sub | FOUND | `Finset.sum_range_sub : ∑ i ∈ range n, (f (i + 1) - f i) = f n - f 0` | `Mathlib.Algebra.BigOperators.Intervals` |
| Big Operators | Finset.sum_range_by_parts | FOUND | `Finset.sum_range_by_parts : ∑ i, f i • g i = ...` | `Mathlib.Algebra.BigOperators.Intervals` |
| Primitive Roots | IsPrimitiveRoot | FOUND | `IsPrimitiveRoot (ζ : M) (k : ℕ) : Prop` | `Mathlib.RingTheory.RootsOfUnity.Basic` |
| Primitive Roots | IsPrimitiveRoot.geom_sum_eq_zero | FOUND | `IsPrimitiveRoot.geom_sum_eq_zero : ∑ i, ζ ^ i = 0` | `Mathlib.RingTheory.RootsOfUnity.Basic` |
| Primitive Roots | Complex.isPrimitiveRoot_exp | FOUND | `Complex.isPrimitiveRoot_exp : IsPrimitiveRoot (exp (2 * pi * I / n)) n` | `Mathlib.Analysis.SpecialFunctions.Complex.RootsOfUnity` |
| Matrices | Matrix.conjTranspose | FOUND | `Matrix.conjTranspose : Matrix m n α → Matrix n m α` | `Mathlib.Data.Matrix.Basic` |
| Matrices | Matrix.kronecker | FOUND | `Matrix.kronecker : Matrix l m α → Matrix n p α → Matrix (l × n) (m × p) α` | `Mathlib.Data.Matrix.Kronecker` |
| Matrices | Matrix.trace_mul_comm | FOUND | `Matrix.trace_mul_comm : (A * B).trace = (B * A).trace` | `Mathlib.Data.Matrix.Basic` |
| Linear Algebra | Module.End | FOUND | `Module.End (R : Type u) (M : Type v) : Type v` | `Mathlib.Algebra.Module.LinearMap.Basic` |
| Linear Algebra | Module.finrank | FOUND | `Module.finrank (R : Type u) (M : Type v) : ℕ` | `Mathlib.LinearAlgebra.Finrank` |
| Algebra | ExteriorAlgebra | FOUND | `ExteriorAlgebra (R : Type u1) (M : Type u2) : Type` | `Mathlib.LinearAlgebra.ExteriorAlgebra.Basic` |
| Algebra | CliffordAlgebra | FOUND | `CliffordAlgebra (Q : QuadraticForm R M) : Type` | `Mathlib.LinearAlgebra.CliffordAlgebra.Basic` |
| Algebra | FreeAlgebra | FOUND | `FreeAlgebra (R : Type u_1) (X : Type u_2) : Type` | `Mathlib.Algebra.FreeAlgebra` |
| Algebra | RingQuot | FOUND | `RingQuot (r : R → R → Prop) : Type uR` | `Mathlib.RingTheory.RingQuot` |
| Algebra | Algebra.adjoin | FOUND | `Algebra.adjoin (s : Set A) : Subalgebra R A` | `Mathlib.Algebra.Algebra.Subalgebra.Basic` |
| Algebra | StarSubalgebra | FOUND | `StarSubalgebra : Type v` | `Mathlib.Algebra.Star.Subalgebra` |
| Algebra | StarAlgHom | FOUND | `StarAlgHom : Type` | `Mathlib.Algebra.Star.StarAlgHom` |
| Algebra | AlgEquiv | FOUND | `AlgEquiv : Type` | `Mathlib.Algebra.Algebra.Equiv` |
| Algebra | Commute | FOUND | `Commute (a b : S) : Prop` | `Mathlib.Algebra.Group.Commute.Basic` |
| MvPolynomials | MvPolynomial | FOUND | `MvPolynomial (σ : Type u_1) (R : Type u_2) : Type` | `Mathlib.Data.MvPolynomial.Basic` |
| MvPolynomials | MvPolynomial.pderiv | FOUND | `MvPolynomial.pderiv (i : σ) : Derivation R (MvPolynomial σ R) (MvPolynomial σ R)` | `Mathlib.Data.MvPolynomial.Derivation` |
| MvPolynomials | MvPolynomial.constantCoeff | FOUND | `MvPolynomial.constantCoeff : MvPolynomial σ R →+* R` | `Mathlib.Data.MvPolynomial.Basic` |
| Power Series | PowerSeries | FOUND | `PowerSeries (R : Type u_1) : Type u_1` | `Mathlib.RingTheory.PowerSeries.Basic` |
| Combinatorics | Nat.Partition | FOUND | `Nat.Partition (n : ℕ) : Type` | `Mathlib.Combinatorics.Partition` |
| Combinatorics | Finset.powerset | FOUND | `Finset.powerset (s : Finset α) : Finset (Finset α)` | `Mathlib.Data.Finset.Powerset` |
| Combinatorics | Finset.sum_bij | FOUND | `Finset.sum_bij : ∑ x ∈ s, f x = ∑ x ∈ t, g x` | `Mathlib.Algebra.BigOperators.Basic` |
| Combinatorics | Finset.card_powerset | FOUND | `Finset.card_powerset : s.powerset.card = 2 ^ s.card` | `Mathlib.Data.Finset.Powerset` |

## Implications for Phase 1

The Mathlib names essential for Phase 1 have been fully audited and are available. Specifically:
- **Bosonization on a Lattice**: The foundational finite-difference structures (`fwdDiff`, `fwdDiff_iter_eq_sum_shift`, etc.) exist in Mathlib out-of-the-box, meaning we can rely on standard theorems instead of building finite-difference calculus entirely from scratch.
- **Algebra and Matrices**: The required structures for representing AQFT fields and operators—such as `StarSubalgebra`, `CliffordAlgebra`, and `Matrix.kronecker`—are supported natively. This allows directly encoding commutation relations and inner products.
- **Identities and Big Operators**: Important summation identities (like `Finset.sum_range_by_parts` and `Finset.sum_bij`) are available, significantly reducing the tedious work of re-proving standard combinatorial shifts when managing interaction terms.

Since all components are currently marked as FOUND, there are no immediate gaps in Mathlib that we need to build ourselves before proceeding with formalization.
