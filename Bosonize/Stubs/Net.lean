import Mathlib
import Bosonize.Stubs.CAR

open Bosonize.Stubs.CAR

set_option linter.dupNamespace false

namespace Bosonize.Stubs.Net

variable (L : ℕ)

abbrev Site (L : ℕ) := Fin L

noncomputable instance {I : Type} : StarRing (Module.End ℂ (Fock I)) := sorry
noncomputable instance {I : Type} : StarModule ℂ (Module.End ℂ (Fock I)) := sorry

def Net (I : Finset (Site L)) : StarSubalgebra ℂ (Module.End ℂ (Fock (Site L))) := sorry

theorem isotony (I J : Finset (Site L)) (h : I ⊆ J) : Net L I ≤ Net L J := sorry

theorem parity_automorphism : True := sorry

theorem twisted_locality (I J : Finset (Site L)) (h : Disjoint I J) (A B : Module.End ℂ (Fock (Site L))) : A * B = B * A := sorry

theorem even_subnet_local : True := sorry

theorem additivity (I J : Finset (Site L)) : Net L (I ∪ J) = Net L I ⊔ Net L J := sorry

theorem translation_covariance : True := sorry

end Bosonize.Stubs.Net
