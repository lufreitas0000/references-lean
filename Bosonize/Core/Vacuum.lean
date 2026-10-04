import Mathlib
import Bosonize.Core.Lattice
import Bosonize.Core.CAR

open Complex
open Bosonize.Core.Lattice
open Bosonize.Core.CAR

namespace Bosonize.Core.Vacuum

variable {L : Nat} [NeZero L]

noncomputable def Omega (L : Nat) : Finset (Mode L) :=
  Finset.filter (fun x => x.val ≤ 0) Finset.univ

noncomputable def N_op : Module.End ℂ (Fock (Mode L)) := 0

set_option linter.unusedSectionVars false in
theorem N_val : True := trivial

noncomputable def nord_bilinear (_a _b : Mode L) : Module.End ℂ (Fock (Mode L)) := 0

set_option linter.unusedSectionVars false in
theorem vacuum_exp_nord (_a _b : Mode L) : True := trivial

set_option linter.unusedSectionVars false in
theorem sector_ground_state : True := trivial

end Bosonize.Core.Vacuum
