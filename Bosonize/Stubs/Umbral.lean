import Mathlib

namespace Bosonize.Stubs.Umbral

variable {R : Type*} [CommRing R]

def shift (f : ℤ → R) : ℤ → R := fun x ↦ f (x + 1)

def fwdDiff (f : ℤ → R) : ℤ → R := fun x ↦ f (x + 1) - f x

def bwdDiff (f : ℤ → R) : ℤ → R := fun x ↦ f x - f (x - 1)

def beta (f : ℤ → R) : ℤ → R := fun x ↦ (x : R) * f (x - 1)

theorem shift_is_aut : True := by sorry

theorem fwdDiff_leibniz (f g : ℤ → R) :
    fwdDiff (fun x ↦ f x * g x) = fun x ↦ fwdDiff f x * g x + shift f x * fwdDiff g x := by
  sorry

theorem sum_by_parts : True := by sorry

theorem umbral_map : True := by sorry

theorem umbral_heisenberg (f : ℤ → R) :
    fwdDiff (beta f) - beta (fwdDiff f) = f := by
  sorry

end Bosonize.Stubs.Umbral
