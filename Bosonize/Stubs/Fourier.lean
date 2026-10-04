import Mathlib

namespace Bosonize.Stubs.Fourier

open Complex

noncomputable def planeWave (zeta : ℂ) (k x : ℤ) : ℂ := zeta ^ (k * x)

theorem sum_planeWave_ortho (L : ℕ) (zeta : ℂ) (h_prim : IsPrimitiveRoot zeta L) (k : ℤ) (h_k : k ≠ 0) (h_mod : k % (L : ℤ) ≠ 0) :
    (Finset.Ico 0 (L : ℤ)).sum (fun x ↦ planeWave zeta k x) = 0 := by
  sorry

theorem dft_unitary : True := by sorry

theorem fwdDiff_planeWave (zeta : ℂ) (k : ℤ) :
    (fun x ↦ planeWave zeta k (x + 1) - planeWave zeta k x) = fun x ↦ (zeta ^ k - 1) * planeWave zeta k x := by
  sorry

end Bosonize.Stubs.Fourier
