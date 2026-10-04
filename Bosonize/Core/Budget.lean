import Mathlib

noncomputable section

namespace Bosonize.Core.Budget

noncomputable def Mode : ℕ → Type := sorry
noncomputable def Omega (L : ℕ) : Finset (Mode L) := sorry
noncomputable def mode_val {L : ℕ} : Mode L → ℤ := sorry
noncomputable def N_val {L : ℕ} : Finset (Mode L) → ℤ := sorry
noncomputable def sector_ground_state {L : ℕ} : ℤ → Finset (Mode L) := sorry

def P_val {L : ℕ} (S : Finset (Mode L)) : ℤ :=
  (S.toList.map mode_val).sum - ((Omega L).toList.map mode_val).sum

noncomputable def e_val {L : ℕ} (S : Finset (Mode L)) (N : ℤ) : ℤ := sorry

theorem e_val_def {L : ℕ} (S : Finset (Mode L)) (N : ℤ) :
  2 * e_val S N = 2 * P_val S - N * (N + 1) := sorry

theorem e_val_nonneg {L : ℕ} (S : Finset (Mode L)) : e_val S (N_val S) ≥ 0 := by sorry

theorem e_val_zero_iff {L : ℕ} (S : Finset (Mode L)) :
  e_val S (N_val S) = 0 ↔ S = sector_ground_state (N_val S) := by sorry

noncomputable def Fock : Type → Type := sorry
noncomputable def C : Type := sorry
noncomputable def BudgetSpace (L K Nmax : ℕ) : Type := sorry

theorem energy_shift_c : True := sorry
theorem energy_shift_cdag : True := sorry

end Bosonize.Core.Budget
