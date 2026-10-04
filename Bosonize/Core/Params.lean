import Mathlib.Algebra.Group.Basic

namespace Bosonize.Core.Params

structure LatticeData where
  L : Nat
  hL : 2 * (L / 2) = L
  hNeZero : NeZero L

structure Window where
  L : Nat
  K : Nat
  Nmax : Nat
  Q : Nat
  h_valid : L > 0

theorem canary_L4_budget_dim : ∃ (w : Window), w.L = 4 := sorry

theorem canary_window_satisfiable : ∃ (w : Window), w.L = 4 := sorry

end Bosonize.Core.Params
