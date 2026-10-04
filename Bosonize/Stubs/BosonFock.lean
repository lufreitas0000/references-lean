import Mathlib

noncomputable section

namespace Bosonize.Stubs.BosonFock

opaque BosonIdx : Type → Type

variable {Q : Type} [DecidableEq (BosonIdx Q)]

opaque a_dag (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ)
opaque a (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ)

opaque J_dag (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ)
opaque J (m : BosonIdx Q) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ)

theorem CCR_a_adag (m m' : BosonIdx Q) :
  a m * a_dag m' - a_dag m' * a m = if m = m' then 1 else 0 := by sorry

opaque vacuum_functional : MvPolynomial (BosonIdx Q) ℂ →ₗ[ℂ] ℂ

opaque number_op_eq_degree : True

opaque weight : MvPolynomial (BosonIdx Q) ℂ → ℕ

opaque sum_lambda_J (lam : BosonIdx Q → ℂ) : Module.End ℂ (MvPolynomial (BosonIdx Q) ℂ)

theorem nilpotent_truncated_exp (K : ℕ) (P : MvPolynomial (BosonIdx Q) ℂ)
  (h : weight P ≤ K) (lam : BosonIdx Q → ℂ) :
  (sum_lambda_J lam ^ (K + 1)) P = 0 := by sorry

end Bosonize.Stubs.BosonFock
