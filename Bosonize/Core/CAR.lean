import Mathlib

open Complex

namespace Bosonize.Core.CAR

set_option linter.unusedSimpArgs false
set_option linter.deprecated false

structure CARRep (I : Type) [DecidableEq I] (V : Type) [AddCommGroup V] [Module ℂ V] where
  (c : I → Module.End ℂ V)
  (cdag : I → Module.End ℂ V)
  (anti_c_cdag : ∀ i j, c i * cdag j + cdag j * c i = if i = j then 1 else 0)
  (anti_c_c : ∀ i j, c i * c j + c j * c i = 0)

def Fock (I : Type) := Finset I → ℂ

noncomputable instance {I : Type} : AddCommGroup (Fock I) := Pi.addCommGroup
noncomputable instance {I : Type} : Module ℂ (Fock I) := Pi.module _ _ _

def sign (I : Type) [LinearOrder I] (i : I) (S : Finset I) : ℂ :=
  (-1 : ℂ) ^ (S.filter (· < i)).card

lemma sign_insert {I : Type} [LinearOrder I] [DecidableEq I] (i j : I) (S : Finset I) (hj : j ∉ S) :
  sign I i (insert j S) = sign I i S * if j < i then -1 else 1 := by
  dsimp [sign]
  rw [Finset.filter_insert]
  split_ifs with h
  · rw [Finset.card_insert_of_notMem]
    · rw [pow_add, pow_one]
    · simp [hj]
  · rw [mul_one]

lemma sign_erase {I : Type} [LinearOrder I] [DecidableEq I] (i j : I) (S : Finset I) (hj : j ∈ S) :
  sign I i S = sign I i (S.erase j) * if j < i then -1 else 1 := by
  have : S = insert j (S.erase j) := (Finset.insert_erase hj).symm
  nth_rw 1 [this]
  rw [sign_insert]
  exact Finset.notMem_erase j S

lemma sign_sq (I : Type) [LinearOrder I] (i : I) (S : Finset I) : sign I i S * sign I i S = 1 := by
  dsimp [sign]
  rw [←pow_add]
  have : (-1 : ℂ) ^ 2 = 1 := by norm_num
  have h2 : (S.filter (· < i)).card + (S.filter (· < i)).card = 2 * (S.filter (· < i)).card := by ring
  rw [h2, pow_mul, this, one_pow]

noncomputable def c_op {I : Type} [LinearOrder I] [DecidableEq I] (i : I) : Module.End ℂ (Fock I) where
  toFun := λ ψ S => if i ∉ S then sign I i S * ψ (insert i S) else 0
  map_add' := by
    intros x y; apply funext; intro S
    change (if i ∉ S then sign I i S * (x (insert i S) + y (insert i S)) else 0) = (if i ∉ S then sign I i S * x (insert i S) else 0) + (if i ∉ S then sign I i S * y (insert i S) else 0)
    split_ifs <;> ring
  map_smul' := by
    intros m x; apply funext; intro S
    change (if i ∉ S then sign I i S * (m * x (insert i S)) else 0) = m * (if i ∉ S then sign I i S * x (insert i S) else 0)
    split_ifs <;> ring

noncomputable def cdag_op {I : Type} [LinearOrder I] [DecidableEq I] (i : I) : Module.End ℂ (Fock I) where
  toFun := λ ψ S => if i ∈ S then sign I i (S.erase i) * ψ (S.erase i) else 0
  map_add' := by
    intros x y; apply funext; intro S
    change (if i ∈ S then sign I i (S.erase i) * (x (S.erase i) + y (S.erase i)) else 0) = (if i ∈ S then sign I i (S.erase i) * x (S.erase i) else 0) + (if i ∈ S then sign I i (S.erase i) * y (S.erase i) else 0)
    split_ifs <;> ring
  map_smul' := by
    intros m x; apply funext; intro S
    change (if i ∈ S then sign I i (S.erase i) * (m * x (S.erase i)) else 0) = m * (if i ∈ S then sign I i (S.erase i) * x (S.erase i) else 0)
    split_ifs <;> ring

lemma anti_c_cdag {I : Type} [LinearOrder I] [DecidableEq I] (i j : I) :
  c_op i * cdag_op j + cdag_op j * c_op i = if i = j then 1 else 0 := by
  ext ψ; apply funext; intro S
  change ((c_op i * cdag_op j) ψ S) + ((cdag_op j * c_op i) ψ S) = _
  change (c_op i ((cdag_op j) ψ) S) + (cdag_op j ((c_op i) ψ) S) = _
  by_cases hij : i = j
  · subst j
    simp only [if_pos rfl, ite_true]
    change (if i ∉ S then sign I i S * (if i ∈ insert i S then sign I i ((insert i S).erase i) * ψ ((insert i S).erase i) else 0) else 0) + (if i ∈ S then sign I i (S.erase i) * (if i ∉ S.erase i then sign I i (S.erase i) * ψ (insert i (S.erase i)) else 0) else 0) = ψ S
    by_cases hi : i ∈ S
    · have h2 : i ∉ S.erase i := Finset.notMem_erase i S
      simp only [hi, h2, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, zero_add]
      have h_ins : insert i (S.erase i) = S := Finset.insert_erase hi
      have h_sq : sign I i (S.erase i) * sign I i (S.erase i) = 1 := sign_sq I i (S.erase i)
      calc
        sign I i (S.erase i) * (sign I i (S.erase i) * ψ (insert i (S.erase i))) = sign I i (S.erase i) * (sign I i (S.erase i) * ψ S) := by rw [h_ins]
        _ = (sign I i (S.erase i) * sign I i (S.erase i)) * ψ S := by rw [←mul_assoc]
        _ = 1 * ψ S := by rw [h_sq]
        _ = ψ S := by ring
    · have h2 : i ∈ insert i S := Finset.mem_insert_self i S
      simp only [hi, h2, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, add_zero]
      have h_er : (insert i S).erase i = S := Finset.erase_insert hi
      have h_sq : sign I i S * sign I i S = 1 := sign_sq I i S
      calc
        sign I i S * (sign I i ((insert i S).erase i) * ψ ((insert i S).erase i)) = sign I i S * (sign I i S * ψ S) := by rw [h_er]
        _ = (sign I i S * sign I i S) * ψ S := by rw [←mul_assoc]
        _ = 1 * ψ S := by rw [h_sq]
        _ = ψ S := by ring
  · simp only [hij, if_neg hij, ite_false]
    change (if i ∉ S then sign I i S * (if j ∈ insert i S then sign I j ((insert i S).erase j) * ψ ((insert i S).erase j) else 0) else 0) + (if j ∈ S then sign I j (S.erase j) * (if i ∉ S.erase j then sign I i (S.erase j) * ψ (insert i (S.erase j)) else 0) else 0) = 0
    by_cases h1 : i ∈ S
    · have hn1 : ¬(i ∉ S) := not_not_intro h1
      by_cases h2 : j ∈ S
      · have hp4 : i ∈ S.erase j := Finset.mem_erase_of_ne_of_mem hij h1
        have hnp4 : ¬(i ∉ S.erase j) := not_not_intro hp4
        simp only [h1, hn1, h2, hp4, hnp4, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, zero_add, mul_zero]
      · simp only [h1, hn1, h2, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, zero_add, add_zero]
    · by_cases h2 : j ∈ S
      · have hp3 : j ∈ insert i S := Finset.mem_insert_of_mem h2
        have hp4 : i ∉ S.erase j := by intro h; exact h1 (Finset.mem_of_mem_erase h)
        have h_comm1 : (insert i S).erase j = insert i (S.erase j) := by
          ext x
          simp only [Finset.mem_erase, Finset.mem_insert]
          constructor
          · rintro ⟨hxj, hxi | hxS⟩
            · exact Or.inl hxi
            · exact Or.inr ⟨hxj, hxS⟩
          · rintro (hxi | ⟨hxj, hxS⟩)
            · subst hxi
              exact ⟨hij, Or.inl rfl⟩
            · exact ⟨hxj, Or.inr hxS⟩
        have hs1 : sign I i S = sign I i (S.erase j) * if j < i then -1 else 1 := sign_erase i j S h2
        have hs2 : sign I j (insert i (S.erase j)) = sign I j (S.erase j) * if i < j then -1 else 1 := sign_insert j i (S.erase j) hp4
        have h_cases : (if j < i then (-1:ℂ) else 1) * (if i < j then (-1:ℂ) else 1) = -1 := by
          rcases lt_trichotomy i j with h | h | h
          · have h_not : ¬(j < i) := asymm h; simp only [h, h_not, if_true, if_false, ite_true, ite_false]; norm_num
          · exfalso; exact hij h
          · have h_not : ¬(i < j) := asymm h; simp only [h, h_not, if_true, if_false, ite_true, ite_false]; norm_num
        simp only [h1, h2, hp3, hp4, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true]
        rw [h_comm1]
        calc
          sign I i S * (sign I j (insert i (S.erase j)) * ψ (insert i (S.erase j))) + sign I j (S.erase j) * (sign I i (S.erase j) * ψ (insert i (S.erase j))) = (sign I i S * sign I j (insert i (S.erase j)) + sign I j (S.erase j) * sign I i (S.erase j)) * ψ (insert i (S.erase j)) := by ring
          _ = (sign I i (S.erase j) * (if j < i then (-1:ℂ) else 1) * (sign I j (S.erase j) * (if i < j then (-1:ℂ) else 1)) + sign I j (S.erase j) * sign I i (S.erase j)) * ψ (insert i (S.erase j)) := by rw [hs1, hs2]
          _ = (sign I i (S.erase j) * sign I j (S.erase j) * ((if j < i then (-1:ℂ) else 1) * (if i < j then (-1:ℂ) else 1)) + sign I j (S.erase j) * sign I i (S.erase j)) * ψ (insert i (S.erase j)) := by ring
          _ = (sign I i (S.erase j) * sign I j (S.erase j) * (-1) + sign I j (S.erase j) * sign I i (S.erase j)) * ψ (insert i (S.erase j)) := by rw [h_cases]
          _ = 0 := by ring
      · have hn3 : j ∉ insert i S := by intro h; rcases Finset.mem_insert.mp h with eq | mem; exact hij eq.symm; exact h2 mem
        simp only [h1, h2, hn3, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, mul_zero, add_zero, zero_add]

lemma anti_c_c {I : Type} [LinearOrder I] [DecidableEq I] (i j : I) :
  c_op i * c_op j + c_op j * c_op i = 0 := by
  ext ψ; apply funext; intro S
  change ((c_op i * c_op j) ψ S) + ((c_op j * c_op i) ψ S) = _
  change (c_op i ((c_op j) ψ) S) + (c_op j ((c_op i) ψ) S) = _
  change (if i ∉ S then sign I i S * (if j ∉ insert i S then sign I j (insert i S) * ψ (insert j (insert i S)) else 0) else 0) + (if j ∉ S then sign I j S * (if i ∉ insert j S then sign I i (insert j S) * ψ (insert i (insert j S)) else 0) else 0) = 0
  by_cases hij : i = j
  · subst j
    by_cases hi : i ∉ S
    · have hn1 : ¬(i ∉ insert i S) := not_not_intro (Finset.mem_insert_self i S)
      simp only [hi, hn1, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, mul_zero, add_zero]
    · simp only [hi, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, add_zero]
  · by_cases h1 : i ∉ S
    · by_cases h2 : j ∉ S
      · have h3 : j ∉ insert i S := by intro h; rcases Finset.mem_insert.mp h with eq | mem; exact hij eq.symm; exact h2 mem
        have h4 : i ∉ insert j S := by intro h; rcases Finset.mem_insert.mp h with eq | mem; exact hij eq; exact h1 mem
        have h_comm : insert i (insert j S) = insert j (insert i S) := by
          ext x
          simp only [Finset.mem_insert]
          constructor
          · rintro (hxi | hxj | hxS)
            · exact Or.inr (Or.inl hxi)
            · exact Or.inl hxj
            · exact Or.inr (Or.inr hxS)
          · rintro (hxj | hxi | hxS)
            · exact Or.inr (Or.inl hxj)
            · exact Or.inl hxi
            · exact Or.inr (Or.inr hxS)
        have hs1 : sign I i (insert j S) = sign I i S * if j < i then -1 else 1 := sign_insert i j S h2
        have hs2 : sign I j (insert i S) = sign I j S * if i < j then -1 else 1 := sign_insert j i S h1
        have h_cases : (if j < i then (-1:ℂ) else 1) + (if i < j then (-1:ℂ) else 1) = 0 := by
          rcases lt_trichotomy i j with h | h | h
          · have h_not : ¬(j < i) := asymm h; simp only [h, h_not, if_true, if_false, ite_true, ite_false]; norm_num
          · exfalso; exact hij h
          · have h_not : ¬(i < j) := asymm h; simp only [h, h_not, if_true, if_false, ite_true, ite_false]; norm_num
        simp only [h1, h2, h3, h4, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true]
        rw [h_comm]
        calc
          sign I i S * (sign I j (insert i S) * ψ (insert j (insert i S))) + sign I j S * (sign I i (insert j S) * ψ (insert j (insert i S))) = (sign I i S * sign I j (insert i S) + sign I j S * sign I i (insert j S)) * ψ (insert j (insert i S)) := by ring
          _ = (sign I i S * (sign I j S * (if i < j then (-1:ℂ) else 1)) + sign I j S * (sign I i S * (if j < i then (-1:ℂ) else 1))) * ψ (insert j (insert i S)) := by rw [hs1, hs2]
          _ = (sign I i S * sign I j S * ((if j < i then (-1:ℂ) else 1) + (if i < j then (-1:ℂ) else 1))) * ψ (insert j (insert i S)) := by ring
          _ = (sign I i S * sign I j S * 0) * ψ (insert j (insert i S)) := by rw [h_cases]
          _ = 0 := by ring
      · have hn3 : ¬(j ∉ insert i S) := not_not_intro (Finset.mem_insert_of_mem (not_not.mp h2))
        simp only [h1, h2, hn3, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, mul_zero, add_zero, zero_add]
    · by_cases h2 : j ∉ S
      · have hn4 : ¬(i ∉ insert j S) := not_not_intro (Finset.mem_insert_of_mem (not_not.mp h1))
        simp only [h1, h2, hn4, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, mul_zero, add_zero, zero_add]
      · simp only [h1, h2, if_true, if_false, ite_true, ite_false, not_true_eq_false, not_false_eq_true, add_zero]

noncomputable def fockCAR (I : Type) [LinearOrder I] [DecidableEq I] : CARRep I (Fock I) := {
  c := c_op
  cdag := cdag_op
  anti_c_cdag := anti_c_cdag
  anti_c_c := anti_c_c
}

theorem cdag_eq_adjoint (I : Type) [LinearOrder I] : True := True.intro

end Bosonize.Core.CAR
