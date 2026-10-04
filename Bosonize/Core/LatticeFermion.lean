import Mathlib
import Bosonize.Core.Lattice
import Bosonize.Core.CAR

open Complex
open Bosonize.Core.Lattice
open Bosonize.Core.CAR

namespace Bosonize.Core.LatticeFermion

variable {L : Nat} [NeZero L]

noncomputable instance : DecidableEq (Site L) := Classical.decEq _
noncomputable instance : DecidableEq (Mode L) := Classical.decEq _

noncomputable def c_pos (j : Site L) : Module.End ℂ (Fock (Mode L)) := sorry

noncomputable def c_pos_CAR : CARRep (Site L) (Fock (Mode L)) := sorry

theorem number_pos_eq_number_mom : True := sorry

noncomputable def tight_binding_H (t : ℂ) : Module.End ℂ (Fock (Mode L)) := sorry

theorem tight_binding_diagonal : True := sorry

theorem tight_binding_umbral : True := sorry

end Bosonize.Core.LatticeFermion
