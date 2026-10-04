import Lean
open Lean Elab Command

def dumpLocks (prefixName : Name) : CommandElabM Unit := do
  let env ← getEnv
  liftCoreM <| Meta.MetaM.run' do
    let opts := (← getOptions).set `pp.all true
    withOptions (fun _ => opts) do
      for (n, cinfo) in env.constants do
        if prefixName.isPrefixOf n then
          let isInteresting := match cinfo with
            | ConstantInfo.thmInfo _ => true
            | ConstantInfo.defnInfo _ => true
            | _ => false
          if isInteresting then
            let typeStr ← Meta.ppExpr cinfo.type
            let typeStrStr := toString typeStr
            IO.println s!"LOCK: {n}\n{typeStrStr}\n---END_LOCK---"

elab "#dump_locks " p:ident : command => do
  dumpLocks p.getId