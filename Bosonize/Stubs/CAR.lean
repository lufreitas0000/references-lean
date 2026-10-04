import Mathlib

open Complex

namespace Bosonize.Stubs.CAR

structure CARRep (I : Type) [DecidableEq I] (V : Type) [AddCommGroup V] [Module ℂ V] where
  (c : I → Module.End ℂ V)
  (cdag : I → Module.End ℂ V)
  (anti_c_cdag : ∀ i j, c i * cdag j + cdag j * c i = if i = j then 1 else 0)
  (anti_c_c : ∀ i j, c i * c j + c j * c i = 0)

def Fock (I : Type) := Finset I → ℂ

noncomputable instance {I : Type} : AddCommGroup (Fock I) := Pi.addCommGroup
noncomputable instance {I : Type} : Module ℂ (Fock I) := Pi.module _ _ _

def fockCAR (I : Type) [LinearOrder I] [DecidableEq I] : CARRep I (Fock I) := sorry

theorem cdag_eq_adjoint (I : Type) [LinearOrder I] : True := sorry

end Bosonize.Stubs.CAR
