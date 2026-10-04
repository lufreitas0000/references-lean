import Lean
open Lean Elab Command

def auditAxioms (prefixName : Name) : CommandElabM Unit := do
  let env ← getEnv
  let allowedAxioms : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let mut foundViolation := false
  for (n, _) in env.constants do
    if prefixName.isPrefixOf n then
      let axioms ← Lean.collectAxioms n
      let mut badAxioms : Array Name := #[]
      for ax in axioms do
        if !allowedAxioms.contains ax then
          badAxioms := badAxioms.push ax
      if !badAxioms.isEmpty then
        logError m!"Unallowed axioms in {n}: {badAxioms}"
        foundViolation := true
  if foundViolation then
    throwError "Unallowed axioms found"

elab "#audit_axioms " p:ident : command => do
  auditAxioms p.getId