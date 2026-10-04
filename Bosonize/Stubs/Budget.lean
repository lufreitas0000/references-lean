import Mathlib

noncomputable section

namespace Bosonize.Stubs.Budget

opaque Mode : ℕ → Type
opaque Omega (L : ℕ) : Finset (Mode L)
opaque mode_val {L : ℕ} : Mode L → ℤ
opaque N_val {L : ℕ} : Finset (Mode L) → ℤ
opaque sector_ground_state {L : ℕ} : ℤ → Finset (Mode L)

def P_val {L : ℕ} (S : Finset (Mode L)) : ℤ :=
  (S.toList.map mode_val).sum - ((Omega L).toList.map mode_val).sum

opaque e_val {L : ℕ} (S : Finset (Mode L)) (N : ℤ) : ℤ

axiom e_val_def {L : ℕ} (S : Finset (Mode L)) (N : ℤ) :
  2 * e_val S N = 2 * P_val S - N * (N + 1)

theorem e_val_nonneg {L : ℕ} (S : Finset (Mode L)) : e_val S (N_val S) ≥ 0 := by sorry

theorem e_val_zero_iff {L : ℕ} (S : Finset (Mode L)) :
  e_val S (N_val S) = 0 ↔ S = sector_ground_state (N_val S) := by sorry

opaque Fock : Type → Type
opaque C : Type
opaque BudgetSpace (L K Nmax : ℕ) : Type

-- energy_shift_c
-- energy_shift_cdag
opaque energy_shift_c : True
opaque energy_shift_cdag : True

end Bosonize.Stubs.Budget
