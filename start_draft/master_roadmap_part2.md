---

## 5. Repository layout and artifacts

```
bosonize-lean/
  lean-toolchain, lakefile.toml, lake-manifest.json     # pinned in Phase 0.1
  docs/
    ROADMAP.md  AGENT_KIT.md
    NOTATION.md                 # notation contract (§8.1)
    MIRANDA_REGISTRY.csv        # one row per Miranda equation (§2)
    WATCHLIST.md                # suspect equations, seeded from Appendix B
    ASSUMPTIONS.md              # the ledger (§4)
    WINDOWS.md                  # window inequalities, one row per theorem
    MATHLIB_AUDIT.md            # every external name used, with #check output
    ENV.md                      # toolchain / Mathlib commit / machine notes
    adr/ADR-000N-*.md           # design decisions
    rfc/RFC-000N-*.md           # post-freeze change requests
    spec/P{p}/S{p}.{s}-<name>.md   (+ .sha256)   # frozen specs
    trace.csv                   # claim <-> spec <-> oracle <-> Lean <-> registry
    gates/G{p}-packet.md        # gate packets for the human
    latex/                      # Phase 7
  oracle/
    oracle_a/                   # implementation A (numpy/scipy, sparse JW matrices)
    oracle_b/                   # implementation B (pure python, occupation sets, exact arithmetic) — different author, different method
    tests/test_<claim-id>.py    # one file per spec claim
    mutants/mut_<claim-id>_*.py # intended-false variants that must FAIL
    reports/<claim-id>.md
  Bosonize/
    Stubs/    # statement-only files; MAY contain sorry; never imported by Core
    Core/     # final Lean; zero sorry; all guards apply
    Continuum/# Tier C only; analysis allowed; not imported by Core
    Audit/    # AuditAxioms.lean, LockDump.lean (guard meta-programs)
  locks/      # statements.lock, defs.lock (hashes)
  ci/         # anti_cheat.sh, notation_lint.py, trace_check.py, run_all.sh
  tests/canary/{good,bad}/   # guard self-tests (§8.9)
```
Core file naming: `Core/<Topic>.lean`, one topic per step cluster; `namespace Bosonize.Core.<Topic>`.

---

## 6. Agent organization

Three groups with separated permissions. **Independence is a design feature**: the groups must not see each other's reasoning, only artifacts.

### 6.1 Blue team (builders)
| Agent | Count | Writes | Never touches |
|---|---|---|---|
| **Orchestrator** (state machine; LLM only for planning and digest writing) | 1 | `gates/`, `trace.csv`, task assignments | any spec/Lean content |
| **Math Formalist** MF-A, MF-B | 2 (independent) | `spec/…` drafts | Lean, oracle |
| **Oracle Engineer** OE-A, OE-B | 2 (independent implementations) | `oracle/oracle_a`, `oracle_b`, tests | specs, Lean |
| **Lean Statement Writer** | 1 | `Bosonize/Stubs/` | proofs, oracle |
| **Lean Prover** LP-1, LP-2 | 2 (competing; first green wins) | `Bosonize/Core/` | statements (locked), oracle |
| **Troubleshooter** | 1–2 | proof fixes in `Core/` | statements |
| **Decomposer** | 1 | proposes sub-lemmas (as new specs) for hard steps | — |
| **Doc/LaTeX Agent** (Phase 7) | 1 | `docs/latex/` | everything else |

### 6.2 Red team (attackers)
| Agent | Attacks | Produces |
|---|---|---|
| **R1 Spec Red-Teamer** | frozen-to-be specs: wrong signs, missing hypotheses, counterexamples | attack report with ≥3 attempted attacks per spec |
| **R2 Notation Auditor** | index/superscript/exponent ambiguity, type of every symbol | `NOTATION` violations list |
| **R3 Numerical Adversary** | random/large parameter search against oracle claims; mutation generation | counterexamples, surviving mutants |
| **R4 Blind Back-Translator** | Lean statements: translates Lean → spec language *without seeing the spec* | back-translation file; diff vs spec |
| **R5 Statement Red-Teamer** | triviality / vacuity / weakness of Lean statements; mutation testing in Lean | list of mutants that Lean cannot distinguish |
| **R6 Proof Auditor** | finished proofs for cheats (§8.8 taxonomy) | audit verdict |
| **R7 Library Verifier** | every Mathlib name used in specs/stubs/proofs against the pinned library | `MATHLIB_AUDIT.md` diffs |
| **R8 Gate Skeptic** | the whole gate packet before the human sees it | "what would a hostile reviewer say" memo |

### 6.3 Referee/infrastructure (non-LLM where possible)
| Component | Function |
|---|---|
| **Gatekeeper** (scripts) | `lake build`, anti-cheat grep, notation lint, axiom audit, statement-lock check, trace check, canary self-test. Returns PASS/FAIL with logs. Cannot be edited by blue or red agents. |
| **Ledger Keeper** | updates `ASSUMPTIONS.md`, `WINDOWS.md`, registry statuses from gate outputs only |

### 6.4 Independence rules
- MF-A and MF-B do not see each other's draft until both are committed; a third agent reconciles.
- OE-A and OE-B implement the oracle from the written spec only; they cross-validate on a shared grid and any disagreement is a bug until resolved.
- R4 never sees the spec for the statement it back-translates.
- Troubleshooter and Provers see statement + error logs + spec, never the oracle code.
- Red agents may not edit blue artifacts; they file findings. Findings have severity `CRITICAL | MAJOR | MINOR`; open CRITICAL blocks the step.

---

## 7. The per-step pipeline ("spec-first loop")

Every step of every phase runs these stages. A stage may not start until the previous gate is green.

| Stage | Who | Output | Gate (hard) |
|---|---|---|---|
| **S0 Claim extraction** | MF-A and MF-B independently | `spec/…md` drafts (template in Kit §K3) with goals, definitions used, explicit hypotheses, statement in the ASCII spec language, Miranda refs with registry status, "what would falsify this" | both drafts exist |
| **S1 Oracle** | OE-A, OE-B, R3 | oracle tests + report on a parameter grid; each claim tested; **mutants** (sign flip, wrong factor, swapped chirality, off-by-one in the window) must fail | all claims pass; all mutants fail; A and B agree |
| **S2 Reconcile + red review** | third MF, R1, R2 | single spec; attack report; notation lint | no CRITICAL; lint clean |
| **S3 Spec freeze** | Gatekeeper | `spec/….sha256` | hash written |
| **S4 Lean statements** | Statement Writer | `Stubs/…lean` (statements only, `sorry` allowed *only here*) | compiles |
| **S5 Fidelity check** | R4 (blind), R5 | back-translation vs spec diff; Lean-level mutation test; non-vacuity witness exists (or is planned) | R4 diff empty modulo notation; no surviving mutant that should be false |
| **S6 Statement lock** | Gatekeeper | `locks/statements.lock`, `locks/defs.lock` (hash of `pp.all` type and of the transitive closure of definitions used) | hashes written |
| **S7 Proof** | LP-1 ∥ LP-2, Troubleshooter | `Core/…lean` with *identical* statement | compiles, no `sorry` |
| **S8 Guards** | Gatekeeper | build, anti-cheat, axiom audit, lock check, canary | all green |
| **S9 Proof audit + trace** | R6, R7, Orchestrator | audit verdict; `trace.csv` row; registry/ledger updates | no CRITICAL |

**Retry budgets**
- Troubleshooter: 12 iterations per lemma. Then the **Decomposer** splits the lemma into ≤5 sublemmas (each goes through S0–S9 as a mini-step, depth ≤ 3).
- If still stuck: the **Specialist loop** (two fresh provers with different strategies + hints from the spec's alternative proof route). Budget: one more full cycle.
- If still stuck: write an **RFC** (§11). The swarm continues with independent steps; it does **not** weaken the statement or add an assumption on its own.

**Statement changes after S6** are only possible through an approved RFC, which sends the step back to S0.

---

## 8. Anti-hallucination and anti-cheat protocol

### 8.1 Notation contract (`docs/NOTATION.md`, written in Phase 0.4, enforced by lint)
The source uses many indices and superscripts (R, L, 1, 2, c, s, †, ν) that collide with exponents. Therefore:
1. **Specs have two layers.** A human layer (LaTeX allowed) and a **machine layer**: ASCII only, in fenced blocks tagged ```` ```spec ````. Lint and Back-Translator operate on the machine layer only.
2. **No bare superscripts in the machine layer.** Exponent is written `pow(x, n)`. Labels are subscripts or named arguments: `b(R, m)`, `bdag(R, m)`, `d(1, m)`, `N(R)`. The dagger is `dag(A)`. The regex `\^` is forbidden in ```` ```spec ```` blocks.
3. **Symbol table.** Every symbol: ASCII name, Lean name, type, domain, whether it may be an exponent (always NO for labels), Miranda glyph(s) it replaces. Distinct meanings get distinct names: chirality label `R|L` vs species label `1|2` (Miranda warns they are not the same), site `j`, band mode `n`, boson index `m`, momentum `q = 2*pi*m/L`.
4. **Typed indices in Lean.** `Site`, `Mode`, `BosonIdx`, `Chirality` are distinct types (or distinct subtypes with distinct names), so swapping `x` and `q` is a type error. `inductive Chirality | R | L`; species labels 1,2 get their own type.
5. **Division and coercions are always typed.** Every `/` and every `(2 : ?)` in a spec names its type (`div_R`, `div_Q`); no `/` in ℕ or ℤ in statements (write `2 * h = L` instead of `h = L / 2`).
6. **Normal-ordering colons** are written `nord(expr)`; no nested colons ever (Miranda's `:(:A::B:):` is ambiguous). Every `nord` states "relative to Omega".
7. **Equation references** use registry IDs (`MIR-045`), never bare `(45)`; Miranda's duplicate numbers (14, 14′, 98, 98′) have distinct IDs.

### 8.2 Miranda registry and watchlist
Phase 0.3 creates the registry (every equation number seen in the three files, plus the missing ones), `WATCHLIST.md` seeded from Appendix B, and strips/labels all transcriber comments. Each equation reaches status `ORACLE-OK` only via an oracle report and `DERIVED-LEAN` only via a gated Lean theorem.

### 8.3 Spec-first and traceability
No Lean before a frozen spec. `trace.csv` columns: `claim_id, spec_path, spec_sha256, oracle_test, mutants_killed, lean_stub_name, lean_core_name, statement_lock_hash, miranda_ids, status`. `ci/trace_check.py` fails if any row is incomplete or any `Core` theorem name is not in the table (no orphan theorems).

### 8.4 Dual numerical oracle
- **Oracle A**: sparse JW matrices (numpy/scipy). **Oracle B**: pure-Python occupation-set implementation with exact arithmetic (fractions / Gaussian rationals where possible; cyclotomic arithmetic or high-precision otherwise). Different authors, different representation. Disagreement beyond 1e-10 (A) or any mismatch (B exact) is a bug in one of them.
- Grid: chiral `L ∈ {4,6,8,10,12}`; two-chirality `L ∈ {4,6,8}` (dim 2^{2L} sparse); all `K, Nmax, Q` consistent with the window; interaction parameters sampled (|λ|<1); also boundary values of windows (equality and equality+1, the latter must fail).
- Oracle tests check **the claim as stated, on the stated domain**, including operator identities on Budget (project with the budget projector) and, where claimed, full-space identities with remainder.
- Seed regression suite: `seed_oracle/` (reproduces Appendix C).

### 8.5 Mutation testing of statements
For each claim the Numerical Adversary generates mutants: sign flips, ±1 shifts of indices/windows, `m` vs `m+1`, `L/2` vs `L/2+1`, swapped R/L, dropped/added `N̂` terms, wrong `2π`/`π` factors, dagger moved. **A claim is accepted only if the original passes and every mutant fails on the oracle.** In Lean, R5 asks whether a mutant could be proved by the same proof; if a mutant *typechecks and is provable*, the statement is too weak or vacuous.

### 8.6 Blind back-translation and the statement lock
R4 converts each Lean statement (and the definitions it uses) into machine-layer spec language without seeing the spec; the diff against the frozen spec must be empty up to notation. The Gatekeeper hashes `pp.all` of the statement **and the transitive closure of definitions** it mentions (so a prover cannot change a definition after the fact). Hashes live in `locks/`.

### 8.7 Banned constructs (grep + meta-program; full list in Kit §K4)
In `Core/`: `sorry`, `admit`, `axiom`, `native_decide`, `opaque`, `unsafe`, `implemented_by`, `extern`, `@[csimp]`, `#exit`, `set_option maxHeartbeats` (any value), `set_option maxRecDepth`, `autoImplicit true`, linter-disabling options, `attribute [local instance]`/`[instance]` outside whitelisted files, `Classical.choose` in *definitions* of model objects, `theorem … : True`, `def … : Prop := True`, `Filter.Tendsto`, `tsum`, `∑'`, `∫`, `deriv`, `MeasureTheory`.
`Stubs/` may contain `sorry`; nothing in `Core/` may import `Stubs/`.

### 8.8 Cheat and failure taxonomy (what R6/R5 hunt)
| Cheat / failure | Detection |
|---|---|
| `sorry` / `axiom` / smuggled axiom via `Classical` or `choice` | grep + `#audit_project` (only `propext`, `Classical.choice`, `Quot.sound`) |
| Weakened statement (fewer cases, extra hypotheses, `∃` instead of explicit formula) | back-translation diff + lock hash |
| **Vacuous hypotheses** (window inequality unsatisfiable, `Fin 0`, `L = 0`, empty budget) | non-vacuity canary `example`s with `Nontrivial`/dimension > 1 |
| Definition tampering (e.g. `b := 0` makes CCR "true") | defs lock; R5 mutation (CCR must fail for a mutated definition) |
| Statement proved for numerals only (`L = 4`) or by `decide` on one case | generality lint: statements must quantify over `L`, `K`, `Q`; at least two distinct parameter points in canaries |
| **Junk values** | dedicated lint list below |
| Shadowed names / wrong namespace | fully-qualified names in locks; R7 checks resolution |
| Unfaithful transcription of Miranda | Miranda is not a source (§2); oracle decides |
| Mathlib name hallucination | R7: name must exist in `MATHLIB_AUDIT.md` with `#check` output |
| Overfitted simp sets / huge `decide` | proof hygiene: no `maxHeartbeats` raise, `decide` only on goals below a size cap, time budget per file |
| Prover edits the oracle or the lock files | file permissions; Gatekeeper checks diff paths |

**Lean junk-value hazards (every spec hypothesis list must address each that applies):**
- `ℕ` subtraction truncates; `ℕ`/`ℤ` division is floor; `L/2` in ℕ.
- `x / 0 = 0` (e.g. `1/√m` at `m = 0`, `λ = ±1`), `Real.sqrt` of a negative number is `0`, `Real.log`/`Complex.log` branch and `log 0 = 0`.
- `ZMod 0 = ℤ`; `Fin n` arithmetic wraps; casts ℤ→ZMod L lose information.
- Empty `Finset.sum = 0`, empty `Finset.prod = 1` (bosonic mode sets with `Q = 0`).
- `Complex.exp` periodicity (phases `e^{2πi n x / L}`) vs integer arguments; `Real.pi` appears only via root-of-unity definitions.
- Coercion hazards ℕ → ℝ → ℂ in sums (`∑ m in range Q` vs `Icc 1 Q` off-by-one).

### 8.9 Guard self-tests (canaries)
`tests/canary/bad/` contains known-bad files (one per banned construct, one with a statement hash mismatch, one with a notation violation, one with an unsatisfiable-window theorem). `tests/canary/good/` contains known-good files. `ci/run_all.sh --selftest` must show **all bad rejected, all good accepted** before any phase proceeds. Guards are re-selftested at every gate.

### 8.10 Library hygiene
Mathlib pinned in `ENV.md`. No `lake update` without an RFC. Every external identifier in specs, stubs, proofs is looked up with `#check`/`#print` by R7 and recorded. Lean API drift (e.g. `collectAxioms` signature) is handled in Phase 0.6 by fixing and re-selftesting the guard scripts.

### 8.11 Resilience against agent drift
Each agent session starts by reading `docs/NOTATION.md`, the spec for its step, and `ASSUMPTIONS.md`; each ends by committing artifacts. Orchestrator tasks quote **file paths and hashes**, not paraphrases. Any paraphrased formula in a task message is ignored: agents must re-read the spec file.
