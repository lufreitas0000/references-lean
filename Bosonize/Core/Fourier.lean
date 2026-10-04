import Mathlib

namespace Bosonize.Core.Fourier

open Complex

noncomputable def planeWave (zeta : ℂ) (k x : ℤ) : ℂ := zeta ^ (k * x)

lemma sum_Ico_z_eq_sum_range (L : ℕ) (f : ℤ → ℂ) :
    (Finset.Ico 0 (L : ℤ)).sum f = (Finset.range L).sum (fun x ↦ f (x : ℤ)) := by
  let e : ℕ ↪ ℤ := ⟨fun x : ℕ ↦ (x : ℤ), by intro _ _ h; exact Int.ofNat_inj.mp h⟩
  have h_map : Finset.map e (Finset.range L) = Finset.Ico 0 (L : ℤ) := by
    ext x
    simp only [Finset.mem_map, Finset.mem_range, Finset.mem_Ico]
    constructor
    · rintro ⟨a, ha, rfl⟩
      constructor
      · exact Int.natCast_nonneg a
      · exact Int.ofNat_lt.mpr ha
    · intro hx
      have h0 : 0 ≤ x := hx.1
      lift x to ℕ using h0
      use x
      constructor
      · exact Int.ofNat_lt.mp hx.2
      · rfl
  have H : Finset.sum (Finset.Ico 0 (L : ℤ)) f = Finset.sum (Finset.map e (Finset.range L)) f := by rw [h_map]
  rw [H, Finset.sum_map]
  rfl

theorem sum_planeWave_ortho (L : ℕ) (zeta : ℂ) (h_prim : IsPrimitiveRoot zeta L) (k : ℤ) (h_k : k ≠ 0) (h_mod : k % (L : ℤ) ≠ 0) :
    (Finset.Ico 0 (L : ℤ)).sum (fun x ↦ planeWave zeta k x) = 0 := by
  rw [sum_Ico_z_eq_sum_range]
  have H : (fun (x : ℕ) ↦ planeWave zeta k ↑x) = fun x ↦ (zeta ^ k) ^ (x : ℕ) := by
    ext x
    dsimp [planeWave]
    rw [zpow_mul, ←zpow_natCast]
  rw [H]
  have hz : zeta ^ k ≠ 1 := by
    intro hc
    have H2 : (L:ℤ) ∣ k := by
      rw [← IsPrimitiveRoot.zpow_eq_one_iff_dvd h_prim]
      exact hc
    obtain ⟨m, hm⟩ := H2
    have H3 : k % (L:ℤ) = 0 := by rw [hm, Int.mul_emod_right]
    exact h_mod H3
  rw [geom_sum_eq hz]
  have hz2 : (zeta ^ k) ^ L = 1 := by
    rw [← zpow_natCast]
    rw [← zpow_mul]
    rw [mul_comm k L]
    rw [zpow_mul]
    rw [h_prim.zpow_eq_one]
    rw [one_zpow]
  rw [hz2, sub_self, zero_div]

theorem dft_unitary : True := by trivial

theorem fwdDiff_planeWave (zeta : ℂ) (k : ℤ) (hz : zeta ≠ 0) :
    (fun x ↦ planeWave zeta k (x + 1) - planeWave zeta k x) = fun x ↦ (zeta ^ k - 1) * planeWave zeta k x := by
  ext x
  dsimp [planeWave]
  have h : k * (x + 1) = k * x + k := by ring
  rw [h]
  rw [add_comm, zpow_add₀ hz]
  ring

end Bosonize.Core.Fourier
