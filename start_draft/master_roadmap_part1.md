# BOSONIZE-LEAN — Master Roadmap v1.0

**Project:** Machine-checked, finite-lattice bosonization of the 1+1D spinless Luttinger model in Lean 4 + Mathlib
**Audience:** Google Antigravity Orchestrator and its agent swarm
**Human supervision:** only at Gates G0 … G7 (end of each phase). Between gates the swarm is autonomous but bound by this document.
**Companion file:** `AGENT_KIT.md` (role prompts, templates, guard scripts). Seed oracle scripts: `seed_oracle/`.

> **Status of this document.** Section 3 ("Design Baseline DB-1") is a *proposal*. It is attacked by the Red team in Phase 0 and frozen at Gate G0. After G0, changes go through the RFC procedure (§11). Everything else is binding from the start.

---

## 0. Operating model

### 0.1 Autonomy and gates
- Agents work without the human between gates. Each phase ends with a **Gate Packet** (§9.G): a ≤2-page auto-generated digest plus links. The human reads the packet, spot-checks, and answers `PASS`, `PASS-WITH-AMENDMENTS`, or `FAIL`. The swarm does not start phase N+1 until it has a `PASS` for phase N.
- **Memory is the repository.** No agent may rely on chat history. Every decision, result and open question is written to a file (spec, ADR, report, ledger) and committed.

### 0.2 Hard stops (any of these halts the swarm and raises a human flag immediately)
1. Any `axiom`, `sorry`, `admit`, `native_decide`, `opaque`, `unsafe`, `implemented_by`, `extern` anywhere in `Bosonize/Core/`.
2. A change to a locked statement or locked definition hash without an approved RFC.
3. The numerical oracle contradicts a frozen spec claim.
4. Two consecutive failed gate attempts inside one phase.
5. Any agent proposes to "assume" a mathematical fact instead of proving or defining it (see §4).

### 0.3 Priorities
Correctness and honesty > traceability > coverage > speed. A smaller theorem set that is fully proved, non-vacuous and faithful beats a bigger one with soft spots.

---

## 1. Mission, scope, definition of done

### 1.1 Mission
Re-derive, **inside Lean 4 with no unproved assumptions beyond Mathlib**, the content of Sections II–XIV and Appendices A–E of E. Miranda, *Introduction to Bosonization*, in a **consistent finite discretization**, and prove the **fermion–boson duality for the simplest interacting spinless model** (the g₂/g₄ Luttinger model of Section XIV): the interacting fermionic Hamiltonian equals an exactly diagonalizable bosonic quadratic Hamiltonian, the diagonalization is an algebra automorphism (Bogoliubov), and the dual-field (g ↔ 1/g) structure and the exact interaction-dependent correlators follow.

Unbounded operators are **not** formalized. They are avoided by construction: (a) the lattice is finite (UV regularization), and (b) states are restricted by an **energy budget** (the physical low-energy restriction). All identities are exact; no limit L→∞ or a→0 appears in the core.

### 1.2 Reference policy
Miranda's text (three OCR files `miranda_1-8.md`, `miranda_9-15.md`, `miranda_16-18.md`) is a **guide, not a source of truth** (§2). Only Miranda and Lean 4/Mathlib are used as references. Claims about external Lean repositories made in earlier planning notes (Physicslib4, OSforGFF, pphi2, "QuantumSystem", etc.) are **unverified and mutually contradictory**; the default is **Mathlib only**. A repository may be used only after Phase 0.2 verifies it exists, pins it, and audits what it provides.

### 1.3 In scope (coverage map; details in Appendix A)
| Miranda part | Work package | Treatment |
|---|---|---|
| §II lattice, BZ, DFT (Eq. 8–16), App. A.1 | P1 | proved (finite Fourier) |
| §III linearized spectrum | P1 | **definition** of the sawtooth-dispersion model on the BZ (an approximation in the source, a definition here) |
| §IV Hilbert space, vacuum, N̂, normal ordering | P1 | constructed finite Fock space, energy filtration |
| §V density operators, bosons (Eq. 42–58) | P2 | exact CCR on budget (+ exact remainder on full space) |
| §VI Haldane completeness (Eq. 59) | P2 | proved on budget (hardest step of the project) |
| §VII, §XII Klein factors (Eq. 60–64, 147–159) | P3 | constructed and proved |
| §VIII–IX Mattis–Mandelstam, chiral fields (Eq. 65–96) | P3 | mode-level / projected identity; finite-sum commutators |
| §X–XI free H₀, two chiralities (Eq. 97–133) | P2/P3/P4 | exact on budget |
| §XIII dual fields φ, θ (Eq. 160–171) | P4 | exact finite sums |
| §XIV.1 Luttinger model, Bogoliubov (Eq. 174–214), App. D | P5 | algebraic automorphism + diagonal form |
| §XIV.2 correlators (Eq. 215–237) | P6 | exact finite formulas incl. g-scaling |
| App. B, C, D, E | P3, P5, P6 | **source text missing** → derived from scratch |
| Eq. 240–247 (dressed Green's function) | Tier C | optional, isolated |

### 1.4 Out of scope
Hubbard/XXZ physics (§II models, §XV Jordan–Wigner/XXZ), spin-½ Luttinger (§XVII), RG/sine-Gordon gaps (§XVIII), Haldane conjecture (§XVI), thermodynamic limit, continuum limit as a theorem (only as optional Tier C), Haag's theorem, GNS/C*-machinery, true unbounded operators, Hilbert-space completions.

### 1.5 Target theorems
Tiers: **A** = must be proved, **B** = proved if Tier A is green and the gate passes, **C** = optional, isolated in `Bosonize/Continuum/`, may use real analysis.

| ID | Name | Miranda ref (guide only) | Tier |
|---|---|---|---|
| T1 | Finite Fourier orthogonality; lattice DFT; CAR in position basis; free tight-binding diagonalization | 8–16, 359–360 | A |
| T2 | Fock space, CAR, vacuum Ω, N-sectors, normal ordering rules | 2, 15, 34–40 | A |
| T3 | Energy filtration and budget subspaces (new; replaces the infinite Dirac sea) | — | A |
| T4 | Density operators: exact CCR with Schwinger term on budget; commutation with N̂; annihilation of ground states | 42–45, 56–58 | A |
| T5 | Sugawara-type identity: P̂ = Σ m b†b + N̂(N̂+1)/2; bosonic form of H₀ | 97–104, 98′ | A |
| T6 | Haldane completeness on budget | 59 | A (fallback in §10) |
| T7 | Klein factors | 60–64, 147–159 | A |
| T8 | Mattis–Mandelstam at mode level / projected form; normal-ordered and un-normal-ordered forms | 65–96 | A |
| T9 | Two-chirality dictionary (R, L), densities, fields | 107–133 | A |
| T10 | Dual fields φ, θ; canonical commutators as exact finite sums; Mandelstam kernel | 160–171 | A (kernel: B) |
| T11 | Luttinger Hamiltonian in bosons (smooth density–density interaction) | 174–182 | A |
| T12 | Bogoliubov automorphism, diagonal form, explicit constant | 183–199, App. D | A |
| T13 | Zero-mode sector diagonalization (N̂, Ĵ) | 214 | A |
| T14 | Duality statements: φ↔θ, g↔1/g, u²=v_N v_J | 209–212, 288–290 | A |
| T15 | Exact correlators: D_c; CDW with g-scaling | 215–237 | B |
| C1 | Limits α→0: sawtooth, log, δ-functions, power-law exponents | 88, 92, 217, 237, App. A.2 | C |
| C2 | Dressed Green's function | 240–247 | C |

### 1.6 Main Theorem (informal; the formal version is written in Phase 6)
For even L and budget parameters satisfying the window inequalities recorded in `docs/WINDOWS.md`:
- **MT1 (kinematics).** The fermionic density modes generate a Heisenberg algebra (with Schwinger term) acting on the budget subspaces; the fermionic sector decomposes into charge sectors, each generated from a ground state by the bosons (T4, T6).
- **MT2 (dictionary).** The fermion field at every lattice site equals the vertex operator built from the bosons, N̂ and Klein factors, on budget (T7, T8, T9).
- **MT3 (Hamiltonian).** The free and interacting fermion Hamiltonians, the latter quartic in fermions, equal explicit bosonic quadratic expressions on budget (T5, T11).
- **MT4 (exact solution).** A Bogoliubov algebra automorphism diagonalizes the bosonic Hamiltonian; the zero-mode sector is diagonalized separately (T12, T13).
- **MT5 (duality).** The φ/θ exchange together with g ↔ 1/g leaves the diagonal Hamiltonian invariant; g = 1 is self-dual (T14).
- **MT6 (observables).** Ground-state density correlators and CDW correlators in the interacting state are exact finite expressions; the CDW correlator equals the free one raised to the power g after normalizing at zero separation (T15).

### 1.7 Definition of done
1. Every Tier A theorem has: a frozen spec, an oracle report, a locked Lean statement, a Lean proof in `Core/` that passes all guards, a trace row.
2. `lake build` from a fresh clone succeeds with zero warnings, zero `sorry`, and `#audit_project Bosonize.Core` shows only `propext`, `Classical.choice`, `Quot.sound`.
3. `docs/ASSUMPTIONS.md` lists the Phase 1 base and **no later additions** (or all additions approved at gates).
4. `docs/trace.csv` has no orphan: every claim ↔ spec ↔ oracle test ↔ Lean name ↔ Miranda registry row.
5. Final Red-team report with no open critical findings.

---

## 2. Truth hierarchy and the status of Miranda

**Order of authority (highest first):**
1. A Lean theorem whose *statement* was locked from a frozen spec and whose proof passes all guards.
2. The exact finite-dimensional **dual oracle** (two independent implementations, §8.4).
3. Two independent agent derivations that agree (MF-A / MF-B).
4. Miranda's text.

**What is wrong with the corpus (verified while preparing this roadmap):**
- All three files are DeepSeek OCR with front-matter `status: machine-transcribed-unverified` and `equation_verification: spot-check failed`.
- Inline blocks starting `> **Comment:**` are **the transcriber's commentary, not Miranda's**. They contain claims of their own (some doubtful). Treat them as untrusted unless re-derived.
- **Missing source text:** Eq. (46)–(55) (page 6 flagged `[UNCLEAR]` and "reconstructed"), Eq. (82)–(83), and **Appendices B, C, D, E entirely**; Appendix A stops after the sawtooth figure of A.2. The `miranda_16-18.md` file ends there. Anything depending on these must be derived from scratch.
- A hand/numerical spot-check already found defects (full list in Appendix B): sign of Eq. (45); Eq. (146) says `[N_ν, N_ν'] = δ`; Eq. (130) lacks the ± between chiralities; Eq. (178) drops the linear term kept in (131)/(168); exponents in (240), (247), (286) look suspect; sign mismatch between (217) and (333).

**Rules**
- No Lean statement or spec may justify itself with "Miranda says". A claim enters the project only with an oracle report and an independent derivation.
- The **Miranda Registry** (`docs/MIRANDA_REGISTRY.csv`) tracks every equation: `UNSEEN | TRANSCRIPTION-SUSPECT | ORACLE-OK | DERIVED-LEAN | CONTRADICTED | MISSING-SOURCE | OUT-OF-SCOPE`.
- Where Miranda is *contradicted*, the project proves the corrected statement and records the discrepancy.

---

## 3. Design Baseline DB-1 (the discretization contract)

> The numbered facts marked **[oracle-seed]** were verified numerically while preparing this roadmap (Appendix C). Facts marked **[hint]** are hand derivations that the Red team must try to break. Nothing here is a theorem until it has passed the pipeline.

### 3.1 Regularization strategy ("consistent discretization")
Two regularizations, used together and everywhere:
1. **Lattice (UV).** Ring of L sites (L even), lattice spacing 1 (Miranda §II convention). Momentum band `I_L = { n ∈ ℤ : −L/2 < n ≤ L/2 }`, `k_n = 2πn/L` (Miranda Eq. 11–12). The position lattice has L points and the band has L modes, so the DFT is exact and **no delta functions, no convergence factor α, no point-splitting are needed**.
2. **Energy budget (degrees of freedom).** Only states with bounded excitation energy above their charge-sector ground state are in the domain of the dictionary identities. This replaces the infinite Dirac sea.

**Parameters:** `L` (even, ≥ 2), budget `K ∈ ℕ`, charge window `Nmax ∈ ℕ`, boson cutoff `Q ∈ ℕ`. A **window inequality** `W(L, K, Nmax, Q)` guarantees that band edges are invisible.

### 3.2 Fock space, vacuum, energy
- One chirality: occupation basis over subsets `S ⊆ I_L`, dimension `2^L`. Vacuum Ω: occupied iff `n ≤ 0` (Miranda Eq. 34). Charge `N(S) = |S| − L/2`, so `|N| ≤ L/2`.
- Momentum `P(S) = Σ_{n∈S} n − Σ_{n≤0, n∈I_L} n` and **excitation energy** `e(S) = P(S) − N(N+1)/2 ∈ ℕ` **[oracle-seed]**: `e ≥ 0`, with equality exactly on the N-sector ground state `|N⟩₀` (fill the lowest `L/2+N` modes).
- A single deep hole at `n = −d` in the vacuum lies in sector N = −1 with `e = d` **[oracle-seed]**. Deep-sea excitations therefore cost energy equal to their depth; this is why band edges are invisible at small budget.
- **Budget subspace** `Budget(L,K,Nmax) = span{ S : e(S) ≤ K, |N(S)| ≤ Nmax }`.
- Two chiralities: one Fock space on `2L` modes `c^R_n, c^L_n`, all mutually anticommuting. Klein-factor signs (Miranda Eq. 149–154) then arise automatically; do not impose a tensor-product convention by hand.

### 3.3 Exactness principle
Every identity of the dictionary is proved in (at most) two forms:
- **(E-full)** an exact operator identity on the whole finite Fock space, with an **explicit remainder** supported at the band edges, when practical; and
- **(E-budget)** the same identity restricted to `Budget(L,K,Nmax)` under a window inequality, where the remainder vanishes.

The symbol `≈` never appears in specs or Lean. Statements are `=` with stated hypotheses.

### 3.4 Seeds for the first theorems
- **[oracle-seed] CCR window.** With `ρ(m) = Σ_{n, n+m ∈ I_L} c†_{n+m} c_n` and `b_m = ρ(−m)/√m`, the relation `[b_m, b†_{m'}] = δ_{m m'}` holds exactly on `Budget(L,K,Nmax)` for all `m, m' ≤ Q` **iff** `Q ≤ L/2 − K − Nmax` (checked L = 12, Nmax ∈ {0,1,2}, K ∈ {0..4}). This is the first entry of `docs/WINDOWS.md`; Phase 2 must prove it and find what is needed for products of several operators.
- **[oracle-seed] Schwinger-term sign.** On the vacuum `⟨[ρ(m), ρ(−m)]⟩ = −m` for `m > 0`. Hence `[ρ(−m), ρ(m)] = +m` on frozen states, matching Miranda (43)–(44) and (120), and **contradicting the sign printed in Eq. (45)**.
- **[hint]** Full-space remainder: `[ρ(−m), ρ(m)] = m − Σ_{bottom m modes}(1 − n_j) − Σ_{top m modes} n_j`.
- **[hint]** `[b_m, b_{m'}] = 0` and `[b_m, N̂] = 0` hold **exactly** with no window (the edge terms cancel under re-indexing). `b_m |N⟩₀ = 0` for all `m ≥ 1`, all N.
- **[hint]** `[P̂, ρ(m)] = m ρ(m)` exactly on the full space, where `P̂ = Σ n :c†_n c_n:`.
- **[oracle-seed] Sugawara.** `P̂ − N̂(N̂+1)/2 = Σ_{m=1}^{L/2−1} m b†_m b_m` held on every budget tested (L = 8, |N| ≤ 1, K ≤ L/2−1) and failed at K = L/2. Direct fermionic proof expected (no completeness needed); Miranda's route (commutator + completeness) is the cross-check.

### 3.5 Replacement table (continuum object → discrete object)
| Continuum / Miranda | Discrete in this project |
|---|---|
| ψ(x), x ∈ ℝ, δ-function anticommutator (31), (118) | ψ_ν(j) = c_{ν,j} on sites j ∈ ℤ_L, Kronecker δ |
| convergence factor `e^{−αq/2}`, α → 0⁺ | none; sharp boson cutoff Q; for the un-normal-ordered vertex operator `α_eff = (L/2π)·e^{−H_Q}`, `H_Q = Σ_{m≤Q} 1/m` **[hint]** |
| `ln`, `arctan`, `sgn` in (87), (88), (91), (92) | the finite sums `S_Q(z) = Σ_{m≤Q} z^m/m` and their real/imaginary parts; limits only in Tier C |
| ∫dx | Σ over sites |
| ∂ₓ of a field | termwise algebraic derivative of the finite trigonometric polynomial (defined algebraically; no `deriv`) |
| point-splitting (95)–(96) | not needed (density at a site is exact) |
| unbounded `exp(i√(2π) φ)` | **nilpotent truncated exponential** on budget: finite sum `Σ_{j≤J} X^j/j!`, equal to the true exponential because `X^{J+1} = 0` on budget |
| ground state of the interacting Hamiltonian | a **state on the boson algebra** (quasi-free, d-vacuum), not a vector of the finite fermion space (§3.8) |
| thermodynamic / continuum limit | not taken (Tier C only) |

### 3.6 Mode-level Mattis–Mandelstam (T8) — the key design insight
Fix budgets `K` (input) and `K'` (output) and `P_K` = orthogonal projector onto `Budget`-type energy ≤ K. The target statement is
`P_{K'} c_x P_K = P_{K'} V_Q(x) P_K`, with `V_Q(x) = L^{-1/2} F z^{N̂} exp(−Σ_{m≤Q} z^{−m}ρ(m)/m) exp(+Σ_{m≤Q} z^{m}ρ(−m)/m)` up to the sign/phase conventions that the oracle must fix, `z = e^{2πi x/L}`.
- **[hint]** In **normal-ordered form** (Miranda 93) the boson cutoff is automatically exact once `Q ≥ max(K, K')`: creation factors of energy > K' are killed by the output projector, annihilation factors of energy > K are killed on the input. No regularization enters the normal-ordered identity.
- **[hint]** Deep-sea terms of `c_x` (modes `n < −K'`) produce energies above K' and are removed by the output projector. This is why the *projected* identity can be exact while the *unprojected* identity cannot: for the full finite band, the eigenvector property of ψ(x)|N⟩₀ fails by bottom-edge terms (these are the UV part of ψ). **Do not try to prove an unprojected finite-band Mattis–Mandelstam formula.**
- The regularization-dependent object is only the un-normal-ordered form (94), via `α_eff`.

### 3.7 Interaction: what the "quartic term" is on a lattice
- **[hint, important]** On a literal lattice, `ψ_ν(j)` are fermions with `ψ² = 0`, so `(ψ†ψ)² = ψ†ψ`: the contact term `g₄ :(ψ†ψ)²:` degenerates to a linear term (Pauli blocking). Miranda's (174) is formal (continuum, point-split). A literal on-site `g₂` term `n^R_j n^L_j` also contains high-momentum parts outside the Luttinger model.
- **Definition (ADR-7 proposal).** Use **smooth (band-limited) densities**
  `ρ^{(Q)}_ν(j) = N̂_ν/L + (1/L) Σ_{1≤m≤Q} (e^{∓iq_m j} ρ_ν(±m) + h.c.-partner)` (signs fixed by the oracle from Miranda 121, to be re-derived),
  and `H_int = Σ_j [ (g₄/2) Σ_ν :(ρ^{(Q)}_ν(j))²: + g₂ :ρ^{(Q)}_R(j) ρ^{(Q)}_L(j): ]`, with `:·:` meaning normal ordering relative to Ω as an explicit definition. This is still a quartic fermion Hamiltonian (a smooth interaction; Miranda notes longer-range interactions are allowed).
- Optional lemma (Tier B): the full lattice `n^R_j n^L_j` differs from the smooth one by terms that vanish or are constants on budget.
- The Red team must also settle the ambiguity of the nested colons in Miranda (174)/(291): compute on the oracle the exact operator difference between `:(ρ²):` and `(:ρ:)²` and record it.

### 3.8 Bogoliubov and the interacting ground state
- **[hint] Algebraic parametrization.** Avoid cosh/sinh/arctanh/sqrt-of-expression junk values by working with `(c, s)` such that `c² − s² = 1`, with `e^{−2γ} = g = (c − s)²`, `e^{γ} = c + s`. The relation `tanh 2γ = λ` becomes `2cs = λ(c²+s²)`. Then `d_1 = c b_R + s b†_L`, `d†_2 = s b_R + c b†_L`; (193) is (183) rewritten.
- **[hint] Hand-check of Miranda 187/188/190.** With `λ = ḡ₂/(1+ḡ₄)`, per mode: off-diagonal terms cancel iff `tanh 2γ = λ`; diagonal coefficient is `√(1−λ²)`; the constant per mode is `q(√(1−λ²) − 1)` (so `H_b = u Σ q d†d + const_Q` with `const_Q = v_F(1+ḡ₄) Σ_{m≤Q} q_m (√(1−λ²) − 1)`). Requires `|λ| < 1` (hazard: Lean `Real.sqrt` returns 0 for negative arguments).
- **[hint]** Mapping (175) → (182) and the zero-mode algebra (214) are algebraically consistent; keep the linear term `(πv_F/L) Σ N̂_ν` that (178) drops.
- **Design consequence.** The exact interacting vacuum is a squeezed state with infinitely many bosons; it is not a vector in the finite fermion space, and any "unitary U_B" would need unbounded generators. Therefore:
  1. Define the **boson algebra** `Heis_Q` abstractly (ADR-5).
  2. Prove the Bogoliubov map is an **`AlgEquiv`** of `Heis_Q`.
  3. Define the interacting vacuum as the **quasi-free state** `ω_d = ω_0 ∘ Θ⁻¹`, where `ω_0` is the Fock vacuum functional (e.g. constant term in the polynomial Fock representation, algebraic) and `Θ` is the automorphism.
  4. All correlators in T15 are `ω_d` of explicit algebra elements.
  The fermion-side identity (MT3) is: on budget, `H_fermion = H_b(b's) + H_N` as maps into the full space (the interaction does not preserve budget).

### 3.9 Vertex operators and expectation values
Truncated exponentials on budget (nilpotent) for the operator identity; **formal power series in an auxiliary parameter** (or a Weyl-type twisted group algebra over a finite-dimensional real symplectic space, ADR-9) for expectation values under `ω_d`. The BCH identities needed are the two standard "Appendix C" identities for a **central commutator**: `e^X e^Y = e^Y e^X e^{[X,Y]}` and `e^{−Y} X e^{Y} = X + [X,Y]`; prove them as algebraic lemmas for nilpotent X, Y in any ℂ-algebra.

### 3.10 What "duality" means formally here
(i) Fermionic H = bosonic H (MT3), (ii) Bogoliubov automorphism with explicit spectrum of the ladder `[H_b, d†] = u q d†` (MT4), (iii) invariance under `(φ, θ, g) → (θ, φ, 1/g)` together with the fact that both `(φ, ∂θ)` and `(θ, ∂φ)` are canonical pairs (MT5), (iv) exact correlators with g-scaling (MT6).

---

## 4. Assumption ledger and the Phase-1 base

**Principle.** The project has **zero axioms**. "Assumptions" are of three kinds only:
1. **Definitions** (e.g. the model, the vacuum, the energy function), recorded in `docs/ASSUMPTIONS.md` with a justification.
2. **Explicit theorem hypotheses**, which must be satisfiable: parameter ranges (`L` even, `0 < m`, `|λ| < 1`, window inequalities).
3. **Mathlib results**, cited by exact name from `MATHLIB_AUDIT.md`.

**Phase 1 builds the base.** At Gate G1 the ledger is frozen. After G1 no new definitions may be added unless they are *derived* from the base or Mathlib, are listed in the ledger with a derivation note, and are reported at the next gate. Candidate base items (final list decided in Phase 0/1): A1 index types and band; A2 primitive root of unity and finite Fourier orthogonality; A3 fermion Fock space with CAR, constructed; A4 vacuum, N̂, ground states |N⟩₀; A5 energy function and budget subspaces; A6 normal ordering relative to Ω; A7 admissible parameter records (`LatticeData`, `Budget`, `Window`); A8 the sawtooth Hamiltonian H₀.

**Non-vacuity rule.** Every `structure`/`class` bundling hypotheses must be **instantiated by a concrete model** in `Core/` (e.g. L = 4, 6). Every theorem family with a window hypothesis must have at least one parameter point where the window is satisfiable *and* the budget space is non-trivial (dimension > 1), proved by a canary `example`.

**Allowed imports.** Mathlib (pinned). Transitive analysis imports (needed for `Real.pi`, `Complex.exp`, `Real.sqrt`) are tolerated; **use** of analysis is not: no `Filter.Tendsto`, `tsum`, `∫`, `deriv`, `MeasureTheory`, `Topology`-based statements in `Core/`. Real analysis lives only in `Bosonize/Continuum/`, which nothing in `Core/` imports.



