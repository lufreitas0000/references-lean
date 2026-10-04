import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Polynomial.Derivative
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

namespace Bosonize

open Finset
open Polynomial

/-- Smoke test 1: Finset sum range succ -/
theorem sum_range_succ_smoke (f : ℕ → ℕ) (n : ℕ) :
    ∑ i ∈ range (n + 1), f i = (∑ i ∈ range n, f i) + f n := by
  exact sum_range_succ f n

/-- Smoke test 2: Polynomial derivative -/
theorem polynomial_derivative_smoke :
    derivative (X ^ 2 : Polynomial ℚ) = 2 * X := by
  simp
  norm_num

/-- Smoke test 3a: ZMod arithmetic -/
theorem zmod_two_smoke (x : ZMod 2) : x + x = 0 := by
  fin_cases x <;> decide

/-- Smoke test 3b: Fin boundary property -/
theorem fin_lt_smoke (n : ℕ) (i : Fin n) : (i : ℕ) < n :=
  i.isLt

/-- Smoke test 4: Matrix commutator in `Matrix (Fin 2) (Fin 2) ℂ` -/
def sigmaX : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def sigmaZ : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

def commutator (A B : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  A * B - B * A

theorem matrix_commutator_smoke :
    commutator sigmaX sigmaZ = !![0, -2; 2, 0] := by
  unfold commutator sigmaX sigmaZ
  rw [Matrix.mul_fin_two, Matrix.mul_fin_two]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply] <;> ring

end Bosonize
