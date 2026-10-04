import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic

/-!
# 1.1 Lattice and Index Types
Defines the spatial geometry and momentum band for the 1D lattice bosonization.
-/

namespace Bosonize

/-- Spatial Lattice Λ (Lambda) as a periodic ring of L sites. -/
def Lambda (L : ℕ) [NeZero L] := ZMod L

/-- Momentum Band Λ* (LambdaDual) as the centered interval of integers. -/
def LambdaDual (L : ℕ) := {n : ℤ // - (L : ℤ) < 2 * n ∧ 2 * n ≤ (L : ℤ)}

/-- Ensures the momentum band is a finite type by mapping it to a bounded interval. -/
instance {L : ℕ} : Fintype (LambdaDual L) :=
  Fintype.ofFinite (LambdaDual L)

/-- 
Coproduct defining the right-moving and left-moving fermion branches.
Initial algebra for F(X) = 1 + 1. 
-/
inductive Chirality
| R
| L
deriving DecidableEq, Repr, Inhabited

end Bosonize
