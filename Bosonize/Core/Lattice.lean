import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Logic.Equiv.Defs

namespace Bosonize.Core.Lattice

def Site (L : Nat) := ZMod L

def Mode (L : Nat) := {n : Int // -L < 2*n ∧ 2*n ≤ L}

inductive Chirality
| R
| L

def modeToFin (L : Nat) (x : Mode L) : Fin L :=
  let M := (L - 1) / 2
  let k : Int := x.val + M
  have h1 : 0 ≤ k := by
    obtain ⟨n, hn⟩ := x
    dsimp [k, M]
    omega
  have h2 : k < L := by
    obtain ⟨n, hn⟩ := x
    dsimp [k, M]
    omega
  ⟨k.toNat, by
    obtain ⟨n, hn⟩ := x
    dsimp [k, M] at *
    omega⟩

def finToMode (L : Nat) (x : Fin L) : Mode L :=
  let M := (L - 1) / 2
  let n : Int := x.val - (M : Int)
  ⟨n, by
    dsimp [n, M]
    have := x.isLt
    omega⟩

def modeEquivFin (L : Nat) : Equiv (Mode L) (Fin L) where
  toFun := modeToFin L
  invFun := finToMode L
  left_inv := by
    intro ⟨n, hn⟩
    dsimp [modeToFin, finToMode]
    apply Subtype.ext
    dsimp
    omega
  right_inv := by
    intro x
    dsimp [modeToFin, finToMode]
    apply Fin.ext
    dsimp
    omega

noncomputable instance (L : Nat) : Fintype (Mode L) :=
  Fintype.ofEquiv (Fin L) (modeEquivFin L).symm

theorem card_mode (L : Nat) (_h : 2 * (L / 2) = L) : Fintype.card (Mode L) = L := by
  rw [Fintype.card_congr (modeEquivFin L)]
  exact Fintype.card_fin L

def modeEquivSite (L : Nat) (_h : 2 * (L / 2) = L) (hPos : L ≠ 0) : Equiv (Mode L) (Site L) :=
  match L, hPos with
  | 0, hp => (hp rfl).elim
  | l + 1, _ => modeEquivFin (l + 1)

end Bosonize.Core.Lattice
