import Mathlib

example : (0:ℂ) ^ (0:ℤ) - (0:ℂ) ^ (-1:ℤ) = ((0:ℂ) ^ (1:ℤ) - 1) * (0:ℂ) ^ (-1:ℤ) := by
  norm_num
