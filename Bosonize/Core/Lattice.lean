import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.Basic

namespace Bosonize.Core.Lattice

/-- Lattice sites are modeled as a cyclic ring of L elements. -/
abbrev Site (L : ℕ) := ZMod L

/-- The momentum band consists of modes n. For simplicity here, modeled as ZMod L. -/
abbrev Mode (L : ℕ) := ZMod L

/-- Chirality index for two-component fermions. -/
inductive Chirality
| R
| L
deriving DecidableEq, Repr

end Bosonize.Core.Lattice
