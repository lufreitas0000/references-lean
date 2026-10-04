import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Logic.Equiv.Defs

namespace Bosonize.Stubs.Lattice

def Site (L : Nat) := ZMod L

def Mode (L : Nat) := {n : Int // -L < 2*n ∧ 2*n ≤ L}

inductive Chirality
| R
| L

noncomputable instance (L : Nat) : Fintype (Mode L) := sorry

theorem card_mode (L : Nat) (h : 2 * (L / 2) = L) : Fintype.card (Mode L) = L := sorry

def modeEquivSite (L : Nat) (h : 2 * (L / 2) = L) : Equiv (Mode L) (Site L) := sorry

end Bosonize.Stubs.Lattice
