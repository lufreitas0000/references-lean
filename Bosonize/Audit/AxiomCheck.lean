import Lean
open Lean Meta Elab Command
def auditProject (pkgName : String) : CommandElabM Unit := do
  IO.println s!"Auditing project {pkgName}... (skipping full check for now)"
