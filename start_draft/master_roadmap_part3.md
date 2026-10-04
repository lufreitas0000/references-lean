---

## 9. Phases

Step IDs are `P.s` (phase.step). Each step runs the §7 pipeline unless marked *infra*. "Hint" = a suggestion the spec authors must verify, not a fact.

### Phase 0 — Infrastructure, truth audit, design freeze  →  Gate G0

**Goal.** Make the swarm trustworthy before any mathematics is formalized.

| Step | Content | Output |
|---|---|---|
| 0.1 *infra* | Pin Lean toolchain and Mathlib commit; empty `Core` builds; sandbox without network; cache. | `ENV.md`, green `lake build` |
| 0.2 | **Library audit.** Verify with `#check`/`#print`: `ZMod`, `Fintype`, `Finset.sum`, `Complex.exp`, `Real.pi`, `IsPrimitiveRoot` and geometric-sum lemmas, `Module.End`, `LinearMap`, `Matrix`/Kronecker products, `PiTensorProduct`, `ExteriorAlgebra`, `CliffordAlgebra` (including contraction), `FreeAlgebra`, `RingQuot`, `MvPolynomial` and `pderiv`, `PowerSeries`, `Nat.Partition`, `LinearIndependent`, `Matrix.conjTranspose`/`star`, Gram–Schmidt/orthogonality on finite-dimensional spaces, any `SymmetricAlgebra`/Weyl-type object. Record presence/absence. Also verify (or refute) the existence of any external repository named in earlier notes; default Mathlib-only. | `MATHLIB_AUDIT.md` |
| 0.3 | **Miranda ingest.** Build the registry from the three files (every equation number, duplicates disambiguated, missing ones flagged). Tag transcriber comments as non-authoritative. Seed `WATCHLIST.md` from Appendix B. | `MIRANDA_REGISTRY.csv`, `WATCHLIST.md` |
| 0.4 | **Notation contract** (§8.1): symbol table, spec language grammar, lint rules; Lean naming scheme and typed-index plan. | `NOTATION.md`, `ci/notation_lint.py` |
| 0.5 | **Dual oracle.** Implement Oracle A and Oracle B; reproduce Appendix C results; cross-validate; provide the budget projector, ρ(m), b_m, P̂, N̂, e(S), and a two-chirality model. | `oracle/…` + report |
| 0.6 *infra* | **Guards.** Implement and compile the Kit scripts (`anti_cheat.sh`, `AuditAxioms.lean`, `LockDump.lean`, `trace_check.py`); build canaries; **self-test must reject all bad canaries.** Fix any Lean API drift. | green `--selftest` |
| 0.7 | **ADRs** (each with ≥3 Red attacks and a rollback plan): see list below. | `adr/ADR-0001…0010` |
| 0.8 | **Windows.** Oracle derives the window inequality needed for each planned Tier A theorem (starting from the CCR seed `Q ≤ L/2 − K − Nmax`); products of two or three operators and the two-chirality case may need larger margins. | `WINDOWS.md` (first version) |
| 0.9 | **Spec of Phase 1** frozen through the full §7 pipeline (S0–S3) so Phase 1 can start immediately after G0. | `spec/P1/*` |

**ADRs to settle in 0.7**
1. **Fock-space representation.** (A) concrete occupation basis `Finset Mode → ℂ` with explicit sign `(−1)^{#{k∈S : k < i}}`; (B) abstract `ExteriorAlgebra`/`CliffordAlgebra` as module with left multiplication and contraction; (C) Jordan–Wigner matrices over a tensor/Kronecker product. Decide by a **spike**: prove CAR for one mode pair in each representation and estimate effort for: vacuum, normal ordering, budget subspaces, two chiralities, adjoint/inner product. Hint: (A) is the favourite for budget subspaces and orthogonality; (B) is attractive for CAR; downstream theorems should depend only on an interface `CARRep` (a `structure` of operators + CAR + vacuum properties) and a **concrete instance** proves non-vacuity.
2. **Index types.** `ℤ`-subtype band vs `Fin L` re-labeling vs `ZMod L`; where wrap-around is allowed.
3. **Normalization.** Unnormalized `J_m = ρ(−m)`, `J†_m` in the core (Heisenberg relation `[J_m, J†_m] = m` — no `√`), with `b_m = J_m/√m` only in a thin adapter. Hint: avoids `Real.sqrt` junk values.
4. **Klein factors.** Primary: Miranda-style definition by action on `b†`-monomials over ground states (needs completeness, T6). Cross-check: explicit shift construction (shift occupied set up by one and fill the bottom edge) with sign. Decide the domain (partial isometry on budget windows).
5. **Boson algebra layer.** `RingQuot (FreeAlgebra …)` modulo CCR vs `MvPolynomial` Fock representation (`b† = multiplication`, `b = pderiv`), and how the vacuum functional is defined.
6. **Vertex/exponential handling.** Truncated nilpotent exponentials on budget; where formal power series are needed.
7. **Interacting Hamiltonian definition** (smooth densities, §3.7), normal-ordering convention, role of the optional Tier B lemma on the literal lattice term.
8. **Bogoliubov parametrization** by `(c, s)` with `c² − s² = 1` (§3.8) and how `g`, `u`, `λ` are derived from physical couplings with hypotheses `|λ| < 1`, `(1+ḡ₄)² > ḡ₂²`.
9. **Correlator machinery.** Weyl-type twisted group algebra over a finite-dimensional real symplectic space vs formal power series; positivity of the state (needed or not).
10. **Junk-value policy.** Hypothesis style, `NeZero`, positivity facts as `Fact`/explicit arguments, ban list from §8.8.

**Gate G0 packet (what the human checks, ≈20 minutes)**
- `--selftest` log: all bad canaries rejected.
- `MATHLIB_AUDIT.md`: spot-check 5 entries; any "absent" item that the design needs.
- `NOTATION.md` symbol table (read it; this is the anti-ambiguity backbone).
- `MIRANDA_REGISTRY.csv` + `WATCHLIST.md`: read the CONTRADICTED/SUSPECT rows.
- ADR summaries: decisions + strongest Red attack for each, and the Red's remaining objections.
- Oracle A/B agreement report on the seed suite.
- `WINDOWS.md` first version.
- Phase 1 specs (names + the ledger draft).
**Pass criteria:** guards proven effective; DB-1 frozen with ADRs; no open CRITICAL.

---

### Phase 1 — Foundations and the assumption base  →  Gate G1
Miranda §II–IV, App. A.1. **Goal:** define every primitive object and prove every "well-known" fact the later phases need. After G1 the ledger is frozen (§4).

| Step | Claim | Notes / hints |
|---|---|---|
| 1.1 | Lattice, band, momenta; parity of L; correspondence band ↔ `ZMod L` | hazards: `L/2` in ℕ, wrap-around; redundancy of `n` beyond the band (MIR-013) |
| 1.2 | Finite Fourier orthogonality: `Σ_{n∈band} z^{nj}`, `Σ_{j∈ℤ_L} ζ^{(n−n')j}` for a primitive L-th root ζ | uses `IsPrimitiveRoot`; Appendix A.1; also (14′) |
| 1.3 | Fermion Fock algebra on `2L` modes (R and L families) with CAR | per ADR-1; prove through the `CARRep` interface and instantiate concretely; exact anticommutators `{c, c†} = δ`, `{c,c} = 0` |
| 1.4 | Lattice fermions `c_j` and DFT: CAR in position basis; `ψ_ν(j) = c_{ν,j}`; unitarity of the transform | exponent-sign conventions of (8) vs (9) differ in the transcription (see watchlist); oracle fixes them |
| 1.5 | Free tight-binding Hamiltonian diagonal in k-space (MIR-016), spinless, any hopping | warm-up, exercises T1 end-to-end |
| 1.6 | Vacuum Ω; N̂; normal ordering relative to Ω as a definition; `⟨nord(·)⟩_Ω = 0`; N-sector ground states `|N⟩₀`, `|N| ≤ L/2`, normalized, mutually orthogonal, with explicit phase convention | Miranda (35)–(40); define the ordered products precisely; sign conventions go into NOTATION |
| 1.7 | Momentum `P̂`, energy `e`, grading; `e(S) ≥ 0` with equality iff ground state; budget subspaces; **energy-shift lemmas** (how `c_n`, `c†_n`, `ρ(m)` change `e` and `N`); closure of budgets | seeds in §3.2; these lemmas make Phases 2–3 tractable |
| 1.8 | Parameter records (`LatticeData`, `Budget`, `Window`), non-vacuity witnesses at `L = 4, 6`, canary theorems, **ledger freeze** | `ASSUMPTIONS.md` |

**Acceptance.** All Tier A claims of T1, T2, T3 green; ledger complete; canaries show non-trivial budget spaces.
**Gate G1 packet:** ledger (read all of it), list of definitions with their locked hashes, T1–T3 trace rows, Red summary, any RFC raised. The human confirms the *definitions are what they intend physically* (vacuum, band, energy, sign conventions) — this is the single most important human review.

---

### Phase 2 — Density operators, bosons, H₀, completeness  →  Gate G2
Miranda §V, VI, X. **Goal:** the Heisenberg algebra inside the fermion Fock space.

| Step | Claim | Notes / hints |
|---|---|---|
| 2.1 | Density operators `ρ_ν(m)`, adjointness `ρ(−m) = ρ(m)†`; exact commutators with `c_p`, `c†_p` including edge terms | basis of Miranda (65)–(66) |
| 2.2 | Full-space CCR with explicit remainder; **budget CCR** (T4) under `Q ≤ L/2 − K − Nmax` (or the sharper inequality found in 0.8); the exact relations `[b_m, b_{m'}] = 0`, `[b_m, N̂] = 0` | hints in §3.4; correct sign of the Schwinger term; replaces MIR-045 as printed |
| 2.3 | `b_m |N⟩₀ = 0` for all m, N | exact; Miranda (57) |
| 2.4 | **Sugawara identity** (T5): `P̂ − N̂(N̂+1)/2 = Σ_m m b†_m b_m` on budget; hence `H₀ = (2πv/L) P̂` has the form (104); ground-state energies `E_N = (π v/L) N(N+1)` (MIR-098′) | Route R1: direct fermionic proof. Route R2 (cross-check): Miranda's commutator + completeness argument |
| 2.5 | Exact commutators `[P̂, ρ(m)] = m ρ(m)` and `[H₀, b†_m] = (2πv m/L) b†_m` on the full space | hint: no window needed |
| 2.6 | **Haldane completeness** (T6) on budget | HARD. Sub-steps: 2.6a Gram matrix of `b†`-monomials over `|N⟩₀`: `⟨b†_λ Ω_N, b†_μ Ω_N⟩ = δ_{λμ} Π_m m^{r_m} r_m!` on budget (needs an inner product on the finite Fock space); 2.6b linear independence of weight-≤K monomials; 2.6c counting: number of sector states with `e = P` equals the number of partitions of P, for `P ≤ L/2 − |N|` (bijection of finite subsets with partitions, Frobenius/boundary-path coordinates); 2.6d spanning by injectivity + equal dimension. Fallback in §10. |
| 2.7 | Consolidation: `WINDOWS.md` updated; registry statuses; hazard review | |

**Acceptance.** T4, T5, T6 green; every window inequality proved (not just stated); mutants of the Schwinger term sign are rejected by Lean-level R5 check.
**Gate G2 packet:** the three headline Lean statements in readable form (R4 back-translation), their window inequalities, the oracle table of window boundary tests (equality passes, +1 fails), and the T6 status (proved / fallback invoked and why).

---

### Phase 3 — Klein factors and Mattis–Mandelstam  →  Gate G3
Miranda §VII, VIII, IX, XI, XII, App. B–C. **Goal:** the fermion field as a vertex operator.

| Step | Claim | Notes / hints |
|---|---|---|
| 3.1 | Klein factors `F, F†` (T7) on budget windows: commute with all `b`, change N by ∓1, `F†|N⟩₀ = |N+1⟩₀`, `[F, N̂] = F`, unitarity relations on the domain | ADR-4; uses T6 for the Miranda-style definition; cross-check with the explicit shift construction |
| 3.2 | Exact `[b_m, c_x]`, `[b†_m, c_x]` with explicit edge term; projected intertwining on budget | basis of Miranda (65)–(67); the edge term does **not** vanish on `|N⟩₀` (it is the UV part) — see §3.6 |
| 3.3 | Truncated exponentials; nilpotency on budget; Appendix C identities (BCH for central commutator; `e^{−Y} X e^{Y} = X + [X,Y]`); coherent-state lemma (Appendix B content, derived) | pure algebra lemmas in an arbitrary ℂ-algebra, then specialized |
| 3.4 | **Projected Mattis–Mandelstam (T8):** `P_{K'} c_x P_K = P_{K'} V_Q(x) P_K` for one chirality (normal-ordered form, MIR-093/123/128); matrix element `⟨N−1|c_x|N⟩₀` (MIR-071) with explicit phase | exact phases/signs from oracle |
| 3.5 | Un-normal-ordered form (MIR-094/129) via the BCH identity, with `α_eff = (L/2π) e^{−H_Q}` (hint); chiral fields `φ_ν`, `φ†_ν`, `φ_ν^{herm}` (two notations of Miranda's `φ` kept apart!) | explicit constants fixed by oracle |
| 3.6 | Field commutators (MIR-086 … 092, 134 … 142) as **exact finite sums** `S_Q`; the density formula `nord(ψ†ψ)(j) = N̂/L ∓ …` (MIR-085/121/130) with the corrected ± | Miranda (130) lacks the ± ; Tier C re-derives the α→0 forms |
| 3.7 | Two chiralities (T9): `ψ_R(x) ~ e^{+ikx}`, `ψ_L(x) ~ e^{−ikx}` conventions (MIR-116, 112); mixed anticommutation; Klein factors `{F_R, F_L} = 0`, `{F†_ν, F_ν} = 2` on the domain, `{F_ν, F_ν'} = 0` for ν ≠ ν′ | with a single `2L`-mode Fock space the signs of Miranda (150)–(154) emerge — prove that they do; correct MIR-146 to `[N̂_ν, N̂_ν'] = 0` |
| 3.8 | Consolidation: registry, windows | |

**Acceptance.** T7, T8, T9 green (single and two chiralities); explicit corrected statements for every CONTRADICTED equation touched.
**Gate G3 packet:** the exact T8 statement with its window, the explicit constant `α_eff`, oracle evidence, a table "Miranda equation → corrected equation → Lean name".

---

### Phase 4 — Free Hamiltonian and dual fields  →  Gate G4
Miranda §X–XI, XIII. **Goal:** H₀ in three equivalent forms and the φ/θ canonical structure.

| Step | Claim | Notes |
|---|---|---|
| 4.1 | `H₀` in the three forms (131), (132), (133) on budget: boson modes, fermion fields, boson fields | (178) vs (131)/(168): keep the `N̂` linear term; (106)/(133) uses the algebraic field derivative |
| 4.2 | Dual fields `φ = (φ_L − φ_R)/√2`, `θ = (φ_L + φ_R)/√2` (MIR-160) and the formulas (161)–(164) | the exponent check `−i√(2π) φ_{R,L} = −i√π(θ ∓ φ)` |
| 4.3 | Canonical commutators (165)–(167) as exact finite sums; `Π = ∂θ`; (168)–(170) | the ± consistency was hand-checked: `[φ, ∂θ] = iδ − i/L` follows from (142); the finite-sum versions come from the oracle |
| 4.4 | *(Tier B)* **Mandelstam kernel**: `(1 − t)·exp(Σ_{m≤Q} t^m/m) ≡ 1 mod t^{Q+1}` (formal power series) and its use to show the statistics transmutation algebraically: `V(z)V(w)` antisymmetry mod high orders | optional second proof of anticommutation, independent of T8 |
| 4.5 | Consolidation | |

**Acceptance.** T10 (Tier A parts) green. **Gate G4 packet:** the three forms of H₀ side by side; φ/θ commutator table with oracle confirmations.

---

### Phase 5 — The interacting spinless model and Bogoliubov  →  Gate G5
Miranda §XIV.1, App. D. **Goal:** the exact solution, inside the algebra.

| Step | Claim | Notes |
|---|---|---|
| 5.1 | Definition of `H_int` with smooth densities (ADR-7); the normal-ordering ambiguity settled by an explicit operator computation (`:(ρ²):` vs `(:ρ:)²`); parameter ranges | the on-site literal term is discussed and (optionally) compared (Tier B lemma) |
| 5.2 | **Fermion → boson** (T11): `H_int = H_int^a + H_int^b` (MIR-175 a,b,c) on budget; `H = H_b + H_N` with `λ` (MIR-182) | oracle checks the constants `ḡ₂ = g₂/(2πv_F)`, `ḡ₄` and the density–density expansion |
| 5.3 | **Bogoliubov algebra** (T12): `d` operators, CCR for `d`, `H_b = u Σ q d†d + const_Q`, explicit `const_Q`, `u`, `g`; inverse transformation (MIR-183 c,d / 195) | hint: parametrize by `(c, s)`; hypotheses `|λ| < 1` |
| 5.4 | Boson algebra `Heis_Q`, automorphism `Θ : AlgEquiv`, ladder relations `[H_b, d†] = u q d†` | ADR-5 |
| 5.5 | Zero-mode sector (T13): `N̂ = N̂_R + N̂_L`, `Ĵ = N̂_R − N̂_L`, `H_N = (π/2L)(u/g N̂² + u g Ĵ²)` plus the linear term; relation `u² = v_N v_J`, `g² = v_J/v_N` (MIR-288–290) | pure algebra |
| 5.6 | Duality (T14): `φ_{1,2}` in terms of `φ, θ, g` (MIR-209), `H_b` in the two forms (212a), (212b), and the exchange `(φ, θ, g) → (θ, φ, 1/g)`; `g = 1` is self-dual | note the transcription of (209a) has `√g θ ∓ φ/√g`; oracle confirms/corrects |
| 5.7 | *(Tier B)* formal-power-series version of the unitary `U_B` (MIR-199) as `Ad` of a formal exponential equal to `Θ` | optional |
| 5.8 | Consolidation | |

**Acceptance.** T11–T14 green. **Gate G5 packet:** headline: "the fermionic interacting H equals the bosonic quadratic H; automorphism; spectrum of the ladder" with the explicit constants, the corrected formulas list, the Red team's strongest remaining objection.

---

### Phase 6 — Correlations and the duality theorem  →  Gate G6
Miranda §XIV.2. **Goal:** exact observables and final theorem.

| Step | Claim | Notes |
|---|---|---|
| 6.1 | Quasi-free state `ω_d = ω_0 ∘ Θ⁻¹` on `Heis_Q`; `ω_d(d_m d†_{m'}) = δ`, `ω_d(d† d) = 0`, Gaussian/Wick property | ADR-5, ADR-9 |
| 6.2 | `D_c(x,y)` (MIR-215–217): exact finite sum, **proportional to g** | hint: `(g/(2πL)) Σ_{m≤Q} q_m 2cos(q_m (x−y))`-type; constants fixed by oracle; the continuum value `−g/(2π²(x−y)²)` is Tier C; note the sign clash with MIR-333 |
| 6.3 | Vertex expectation machinery: BCH in the d-basis; CDW operator (MIR-218–236) | uses §3.9 |
| 6.4 | **CDW correlator** (T15): exact finite expression, and the exact statement `ln ω_d(r) − ln ω_d(0) = g · (ln ω_free(r) − ln ω_free(0))` | hint, derived by hand from (234): `X+Y = (g−1)[V,V†]`; must be verified by oracle and then proved; the free case is `g = 1` |
| 6.5 | **Main Theorem** assembly: formal statements MT1–MT6, the "duality dictionary" table (fermionic observable ↔ bosonic expression), proofs referencing earlier theorems only | |
| 6.6 | *(Tier C, only after G6 approval)* limits: α→0 forms (88), (92), (217), the power law (237) with exponent `2g`, Appendix A.2 sawtooth via Mathlib's Fourier/Bernoulli facts if available; the dressed Green's function (240)–(247) with its suspicious exponents re-derived | isolated in `Continuum/` |

**Acceptance.** T15 and MT assembled, or an honest statement of exactly which parts are green. **Gate G6 packet:** the formal MT statement in readable form, trace matrix, list of all Miranda discrepancies found.

---

### Phase 7 — Consolidation, audit, documentation  →  Gate G7 (final)
| Step | Content |
|---|---|
| 7.1 | Fresh-clone reproducibility: `lake build`, guards, selftest, oracle suite |
| 7.2 | Global Red audit: every theorem, every definition, every ledger entry, every lock; independent re-derivation of three random Tier A results by an agent that did not work on them |
| 7.3 | Coverage matrix (Appendix A) completed: each Miranda equation with its final status |
| 7.4 | LaTeX report (Kit §K2 prompt): per theorem, what was proved, what Miranda got wrong, the discretization dictionary, and a *Continuum interpretation* subsection explicitly labeled **conceptual, not formalized** |
| 7.5 | README, limitations, "what would be needed for Tier C and for the continuum limit" |

**Gate G7 packet:** final trace matrix, audit verdict, list of Miranda corrections, open problems.

---

## 10. Risk register and fallbacks

| Risk | Likelihood | Mitigation / fallback |
|---|---|---|
| **T6 Haldane completeness stalls** (partition ↔ finite-subset bijection, Gram matrix) | high | Decomposer + Specialist loop; alternative route via Schur-function/Murnaghan–Nakayama combinatorics; or reduce to a **smaller explicit budget** `K ≤ K₀` with a uniform proof by induction on `K` (still all `L`); supervisor decides at G2. Under no circumstance replace it by an assumption. Items downstream of T6 (T7 definition, T8) can use the explicit-shift Klein construction as an independent route, which does not need T6 for existence but still needs it for the intertwining on all budget states. |
| Fock-space representation chosen in ADR-1 proves too painful | medium | `CARRep` interface isolates the choice; switch representation by re-instantiating |
| Lean performance (dimension 2^{2L}) | medium | proofs are generic in L; never `decide` on large instances; budgets small by design |
| Window inequality differs from oracle seed once two or more operators are composed | high | `WINDOWS.md` is updated by proof, not by guess; theorems carry the proved inequality |
| Weyl/Gaussian state positivity | medium | not needed if correlators are formulated as formal-series identities (ADR-9) |
| Mathlib gaps (no Weyl algebra, no Fock space, no `SymmetricAlgebra` of the needed type) | medium | built in-project from `FreeAlgebra`/`RingQuot`/`MvPolynomial`; recorded in the audit |
| Miranda errors propagate | high | §2 rules; registry; oracle first |
| Agent drift / notation drift | high | §8.1, §8.11; lints |
| Guard scripts rot with Lean updates | low | Mathlib pinned; selftest at each gate |

---

## 11. Escalation, RFC and stop rules
- **RFC** (template in Kit): any change to a frozen spec, a locked statement, a definition in the ledger, a window inequality, or an ADR. Requires: motivation, impact list (trace rows), Red review, and goes to the next gate packet. CRITICAL-impact RFCs (definition or statement of a Tier A theorem) raise a human flag immediately.
- **Stop-and-ask triggers:** §0.2, plus an agent being unable to prove a Tier A statement after the retry budgets (§7), plus oracle/spec contradictions.
- Never allowed: weakening a statement, adding an assumption, editing a lock, editing the oracle to make a test pass, or marking a registry row `ORACLE-OK` without a report.
- If time or budget runs out: declare the highest fully green tier; do not ship partially proved theorems under the project name.

---

## Appendix A — Miranda coverage matrix (initial; Phase 0.3 expands to every equation)
| Miranda eq. (as printed) | Content | WP | Initial status |
|---|---|---|---|
| 1, 2a/b, 4–7 | Hubbard/Heisenberg definitions, c-CAR | P1 (CAR only) | context |
| 8–16, 14′ | DFT, BZ, free hopping | P1 | to derive; (8) transcription typo noted by transcriber |
| 17–19 | filling, Fermi sea | context | out of scope |
| 22–29, 31 | linearized branch, ψ(x) | P1 (definition), P3 | δ-function → Kronecker |
| 33–40 | vacuum, N̂, normal order, ground states | P1 | to derive |
| 41 | `H = ⊕ H_N` | P1/P2 | to derive on budget |
| 42–45, 56–58 | ρ(q), b_q, CCR, annihilation | P2 | **45 contradicted (sign)**; 46–55 **missing source** |
| 59 | completeness | P2 | to derive (T6) |
| 60–64 | Klein factors | P3 | to derive |
| 65–81 | MM derivation | P3 | to derive; 82–83 **missing** |
| 84–96 | fields, MM forms, commutators | P3 | to derive finite versions; Tier C limits |
| 97–106 | H₀ | P2/P4 | to derive |
| 107–133 | lattice→linear model, chiral dictionary | P3/P4 | 130 **suspect**; 120–121 to check |
| 145–159 | multi-species Klein | P3 | **146 contradicted** |
| 160–171 | dual fields | P4 | to derive |
| 172–182 | Luttinger model | P5 | 174 ambiguity; 178 **suspect** |
| 183–199 | Bogoliubov | P5 | hand-checked consistent (187, 188, 190); to derive |
| 203–214 | new fields, H_N | P5 | to derive |
| 215–217 | D_c | P6 | to derive |
| 218–237 | CDW correlator | P6 | to derive; 223, 231–236 to check |
| 240–247 | Green's function | Tier C | **suspect exponents** |
| 248–344 | consequences, spin, XXZ | — | out of scope |
| 345–358 | gaps, sine-Gordon | — | out of scope |
| A.1, A.2 | sums, periodic δ | P1, Tier C | A.1 to derive; A.2 text truncated |
| B, C, D, E | coherent states, identities, Bogoliubov, Green's function | P3, P5, P6 | **source text missing** |

## Appendix B — Watchlist seeded by the supervisor-side reading
(Hand/numerical checks only; none is authoritative. Each row must be re-established by the oracle in Phase 0.3/0.5.)

| ID | Eq. | Finding | Verdict |
|---|---|---|---|
| W-01 | 45 | Printed `[ρ(q), ρ(q′)] = +(Lq/2π) δ_{q+q′,0}`. With `ρ(q) = Σ c†_{k+q} c_k`, `q>0`, vacuum with `k ≤ 0` filled, `⟨[ρ(q), ρ(−q)]⟩ = −Lq/2π` (oracle seed). Eq. (43), (44), (120) are consistent with the minus sign. | printed sign wrong, or convention clash |
| W-02 | 146 | `[N̂_ν, N̂_ν′] = δ_{νν′}` | wrong; should be 0 |
| W-03 | 130 vs 121/162 | `:ψ†_{R,L}ψ_{R,L}: = N̂/L + (1/√2π) ∂φ_{R,L}` has the same sign for R and L; Eq. (85) has a minus sign for a single branch; (162)–(164) distinguish ± | inconsistent; derive |
| W-04 | 178 vs 131, 168 | `(πv_F/L) Σ N̂²` drops the linear term `(πv_F/L) Σ N̂` | inconsistent; keep the linear term |
| W-05 | 187, 188, 190 | Bogoliubov: off-diagonal cancels iff `tanh 2γ = λ`; diagonal `√(1−λ²)`; `g = e^{−2γ}`; constant per mode `q(√(1−λ²) − 1)` | consistent (hand-check); constant not stated by Miranda |
| W-06 | 175 → 182 | mapping of `g₂`, `g₄` terms to `b`-operators | consistent up to L-convention (hand-check) |
| W-07 | 214 | `H_N` decomposition into `N̂`, `Ĵ` | algebraically consistent |
| W-08 | 98′ | `E_N = (π/L) N(N+1)` for both signs of N | consistent |
| W-09 | 167 vs 142 | `[φ, ∂θ] = iδ − i/L` follows from the chiral commutators | consistent |
| W-10 | 217 vs 333 | `D_c = −g/(2π²(x−y)²)` vs `+g_c/(πx)²` | sign/normalization clash (spinless vs spinful?) |
| W-11 | 240, 247 | exponents `(1/4)(1/2+g)`, `(1/4)(1/2+g−2)` look inconsistent with (341), (344) | suspect; Tier C |
| W-12 | 286 | transcriber already flags the exponent; unresolved | suspect; out of scope |
| W-13 | 174, 291 | nested normal ordering ambiguity; plus lattice fact `(ψ†ψ)² = ψ†ψ` (§3.7) | definition needed (ADR-7) |
| W-14 | 156 | `{F†_ν, F_ν′} = 2δ` holds only where F is unitary; finite band: partial | restate on domain |
| W-15 | 8–9 | transcriber notes sign typos in the DFT lines | oracle fixes conventions |
| W-16 | header notes | the transcriber's `> Comment:` blocks (e.g. on kinks, anomalous dimensions, nested colons) are not Miranda's | untrusted |

## Appendix C — Seed oracle results (reproducible with `seed_oracle/*.py`)
- Jordan–Wigner CAR check passes (L = 8).
- Vacuum expectation `⟨[ρ(m), ρ(−m)]⟩ = −m` for m = 1, 2, 3 (L = 8).
- `e(S) ≥ 0` over all 256 basis states (L = 8); a single hole at depth d in the vacuum has `e = d`.
- Sugawara-type identity `P̂ − N̂(N̂+1)/2 = Σ_{m=1}^{L/2−1} m b†_m b_m` exact on budget for K ≤ 3 at L = 8 (|N| ≤ 1), fails at K = 4 = L/2.
- CCR window: for L = 12, |N| ≤ Nmax ∈ {0,1,2}, K ∈ {0,…,4}, the largest Q with exact `[b_m, b†_{m′}] = δ` on all budget vectors is exactly `L/2 − K − Nmax`.
These are single-chirality, single-lattice checks. They support but do not replace Phase 0.5.
