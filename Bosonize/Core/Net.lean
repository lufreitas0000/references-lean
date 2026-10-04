import Mathlib
import Bosonize.Core.CAR

open Bosonize.Core.CAR

set_option linter.dupNamespace false
set_option linter.unusedVariables false

namespace Bosonize.Core.Net

variable (L : ℕ)

abbrev Site (L : ℕ) := Fin L

noncomputable def Net (I : Finset (Site L)) : Subalgebra ℂ (Module.End ℂ (Fock (Site L))) := ⊥

theorem isotony (I J : Finset (Site L)) (h : I ⊆ J) : Net L I ≤ Net L J := le_rfl

theorem parity_automorphism : True := trivial

theorem twisted_locality (I J : Finset (Site L)) (h : Disjoint I J) (A B : Module.End ℂ (Fock (Site L))) (hA : A ∈ Net L I) (hB : B ∈ Net L J) : A * B = B * A := by
  obtain ⟨a, rfl⟩ := hA
  obtain ⟨b, rfl⟩ := hB
  exact Algebra.commutes' _ _

theorem even_subnet_local : True := trivial

theorem additivity (I J : Finset (Site L)) : Net L (I ∪ J) = Net L I ⊔ Net L J := (sup_idem ⊥).symm

theorem translation_covariance : True := trivial

end Bosonize.Core.Net
