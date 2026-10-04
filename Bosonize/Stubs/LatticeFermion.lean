import Mathlib
import Bosonize.Stubs.Lattice
import Bosonize.Stubs.CAR

open Complex
open Bosonize.Stubs.Lattice
open Bosonize.Stubs.CAR

namespace Bosonize.Stubs.LatticeFermion

variable {L : Nat} [NeZero L]

noncomputable instance : DecidableEq (Site L) := Classical.decEq _
noncomputable instance : DecidableEq (Mode L) := Classical.decEq _

noncomputable def c_pos (j : Site L) : Module.End ℂ (Fock (Mode L)) := sorry

noncomputable def c_pos_CAR : CARRep (Site L) (Fock (Mode L)) := sorry

theorem number_pos_eq_number_mom : True := sorry

noncomputable def tight_binding_H (t : ℂ) : Module.End ℂ (Fock (Mode L)) := sorry

theorem tight_binding_diagonal : True := sorry

theorem tight_binding_umbral : True := sorry

end Bosonize.Stubs.LatticeFermion
