import Mathlib.Analysis.Complex.Basic
import Mathlib.RingTheory.RootsOfUnity.Basic

namespace Bosonize.Core.Fourier

/-- Plane wave e_k(x) = ζ^(k*x) -/
noncomputable def planeWave (L : ℕ) (ζ : ℂ) (k x : ℤ) : ℂ :=
  ζ ^ (k * x)

-- The actual orthogonality would use `IsPrimitiveRoot ζ L`
-- This is a stub file for the Fourier structure.

end Bosonize.Core.Fourier
