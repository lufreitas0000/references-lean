import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Data.Fintype.Basic

namespace Bosonize.Core.Umbral

variable {R : Type} [CommRing R]

/-- The shift operator on functions. -/
def shift (f : ℤ → R) : ℤ → R :=
  fun x => f (x + 1)

/-- The forward difference operator. -/
def fwdDiff (f : ℤ → R) : ℤ → R :=
  fun x => f (x + 1) - f x

/-- The backward difference operator. -/
def bwdDiff (f : ℤ → R) : ℤ → R :=
  fun x => f x - f (x - 1)

/-- The multiplication by x operator. -/
def beta (f : ℤ → R) : ℤ → R :=
  fun x => x * f (x - 1)

end Bosonize.Core.Umbral
