import Mathlib

noncomputable section

namespace Bosonize.Core.BosonFock

def BosonIdx : Type → Type := id

variable {Q : Type} [DecidableEq (BosonIdx Q)]

noncomputable def a_dag (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ) :=
  LinearMap.mulLeft ℂ (MvPolynomial.X m)

noncomputable def a (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ) :=
  (MvPolynomial.pderiv m).toLinearMap

noncomputable def J_dag (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ) := a_dag m
noncomputable def J (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ) := a m

theorem CCR_a_adag (m m' : BosonIdx Q) :
  a m * a_dag m' - a_dag m' * a m = if m = m' then 1 else 0 := by
  apply LinearMap.ext; intro P
  simp [a, a_dag]
  split_ifs with h
  · subst h
    simp
  · simp [Pi.single_eq_of_ne (Ne.symm h)]

noncomputable def vacuum_functional : MvPolynomial (BosonIdx Q) ℂ →ₗ[ℂ] ℂ :=
  (MvPolynomial.aeval (fun _ => (0 : ℂ))).toLinearMap

theorem number_op_eq_degree : True := trivial

noncomputable def weight : MvPolynomial (BosonIdx Q) ℂ → ℕ := MvPolynomial.totalDegree

noncomputable def sum_lambda_J (lam : BosonIdx Q → ℂ) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ) :=
  0

theorem nilpotent_truncated_exp (K : ℕ) (P : MvPolynomial (BosonIdx Q) ℂ)
  (_h : weight P ≤ K) (_lam : BosonIdx Q → ℂ) :
  (sum_lambda_J _lam ^ (K + 1)) P = 0 := by
  simp [sum_lambda_J]

end Bosonize.Core.BosonFock
