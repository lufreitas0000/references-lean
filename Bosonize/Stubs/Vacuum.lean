import Mathlib
import Bosonize.Stubs.Lattice
import Bosonize.Stubs.CAR

open Complex
open Bosonize.Stubs.Lattice
open Bosonize.Stubs.CAR

namespace Bosonize.Stubs.Vacuum

variable {L : Nat} [NeZero L]

noncomputable def Omega (L : Nat) : Finset (Mode L) := sorry

noncomputable def N_op : Module.End ℂ (Fock (Mode L)) := sorry

theorem N_val : True := sorry

noncomputable def nord_bilinear (a b : Mode L) : Module.End ℂ (Fock (Mode L)) := sorry

theorem vacuum_exp_nord (a b : Mode L) : True := sorry

theorem sector_ground_state : True := sorry

end Bosonize.Stubs.Vacuum
