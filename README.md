# BOSONIZE-LEAN — Lattice AQFT Bosonization in 1+1D, Umbral-Regularized and Lean 4–Verified

> Markdown + LaTeX notes on **bosonization in 1+1 dimensions**, built on a **lattice-regularized
> algebraic QFT (AQFT)** and written in the language of **umbral (finite-difference) calculus**, so
> that every theorem can be machine-checked in **Lean 4 + Mathlib**. No unbounded operators appear
> anywhere in the formal layer.

---

## 1. What this project is

The standard continuum treatment of bosonization (Mattis–Mandelstam, Haldane, Miranda's
*Introduction to Bosonization*) manipulates objects that are *not* well defined as written:
unbounded field operators $\phi(x)$, $\partial_x\phi$, vertex operators $e^{i\sqrt{4\pi}\phi}$,
δ-function anticommutators, an infinite Dirac sea, and limits $\alpha\to0^+$.

This project re-derives the theory so that **every statement is an exact identity between
finite-dimensional or purely algebraic objects**:

| Continuum object (ill-defined) | Replacement here (well-defined, Lean-checkable) |
|---|---|
| space $\mathbb{R}$, $\int dx$ | ring $\mathbb{Z}_L$ of $L$ sites, $\sum_j$ |
| derivative $\partial_x$ | **umbral delta operators** $\Delta = E-1$, $\nabla = 1-E^{-1}$ (shift $E$) |
| $[\partial_x, x] = 1$ (unbounded CCR) | **umbral Heisenberg pair** $[\Delta,\, x E^{-1}] = 1$ on lattice functions / polynomials |
| local field algebras on open sets | **lattice AQFT net** $I\mapsto\mathfrak A(I)$, $I\subseteq\mathbb Z_L$ (isotony, twisted locality) |
| boson Fock space (unbounded $b,b^\dagger$) | polynomial (Bargmann–umbral) representation: $b^\dagger = $ multiplication, $b = $ formal derivative on $\mathbb C[x_1,\dots,x_Q]$ |
| infinite Dirac sea | finite band + **energy budget** subspaces |
| $e^{X}$ with unbounded $X$ | **nilpotent truncated exponentials** on budget / formal power series |
| $\delta$-functions, $\ln$, $\operatorname{sgn}$ in correlators | Kronecker δ and exact finite sums $S_Q(z)=\sum_{m\le Q} z^m/m$ |
| continuum limit $a\to0$, $L\to\infty$ | **not formalized** (documented as interpretation only; optional Tier C) |

Lean has no notion of "domain of an unbounded operator" in the algebraic layer: all operators are
`Module.End`s of finite-dimensional spaces or of polynomial modules, and every identity is `=`
with explicit hypotheses — never `≈`.

## 2. Mathematical backbone

1. **Umbral calculus on the lattice.** Shift $E$, difference operators $\Delta,\nabla$, discrete
   Leibniz rule $\Delta(fg) = (\Delta f)g + (Ef)(\Delta g)$, summation by parts, falling factorials
   $x^{\underline n}$ with $\Delta x^{\underline n} = n x^{\underline{n-1}}$, the umbral map
   $x^n\mapsto x^{\underline n}$ intertwining $d/dx$ with $\Delta$, and Fourier diagonalization
   $\Delta e_k = (\zeta^k-1)e_k$. Mathlib already provides `fwdDiff` and `descPochhammer`.
2. **Lattice AQFT.** The CAR algebra on $\mathbb Z_L$ (two chiralities) as a net of local
   $*$-algebras indexed by finite regions, with isotony, **graded (twisted) locality**, parity
   grading, and the even (observable) subnet. Bosonization is formulated *inside* this net.
3. **Bosonization dictionary** (following Miranda §II–XIV as a *guide, not as a source of truth*):
   density modes → Heisenberg algebra with Schwinger term on budget; Haldane completeness; Klein
   factors; projected Mattis–Mandelstam formula; free and interacting (Luttinger) Hamiltonians;
   Bogoliubov automorphism; φ/θ duality $g\leftrightarrow 1/g$; exact finite correlators.

## 3. Outputs

- **Lean 4 library** `Bosonize/` — zero `sorry`, zero `axiom` in `Bosonize/Core/`; only
  `propext`, `Classical.choice`, `Quot.sound` in `#print axioms`.
- **Markdown notes** `notes/md/` — one note per step (definitions, statements, proofs, Lean names).
- **LaTeX notes** `notes/tex/` — the same content as a typeset document with a
  "Continuum interpretation (not formalized)" subsection per chapter.
- **Numerical oracle** `oracle/` — exact/sparse finite-dimensional checks of every claim before
  it is formalized.

## 4. Repository layout

```
references-lean/
  README.md                 # this file
  roadmap_v1.0.0.md         # overview roadmap (phases 0–7, gates)
  phase01.md                # detailed plan: Phase 0 (environment) and Phase 1 (foundations)
  start_draft/              # earlier planning drafts (historical; superseded by the files above)
  lean-toolchain, lakefile.toml, lake-manifest.json   # pinned Lean + Mathlib
  Bosonize.lean             # library root
  Bosonize/
    Basic.lean              # smoke tests (Phase 0)
    Core/                   # final proofs — all guards apply
    Stubs/                  # locked statements, may contain sorry; never imported by Core
    Continuum/              # Tier C only (analysis allowed); never imported by Core
    Audit/                  # axiom audits, lock dumps
  docs/                     # ENV, NOTATION, ASSUMPTIONS, WINDOWS, MATHLIB_AUDIT, ADRs, specs, gates
  notes/md/  notes/tex/     # the human-readable notes
  oracle/                   # Python numerical oracle (uv venv) + tests
  scripts/                  # check_env.sh, guards, gemini helper
  tests/canary/{good,bad}/  # guard self-tests
```

## 5. Quickstart

```bash
# Lean (elan is installed user-locally in ~/.elan)
source ~/.elan/env
lake exe cache get        # prebuilt Mathlib oleans
lake build                # build the library
scripts/check_env.sh      # versions + build + anti-cheat grep

# Numerical oracle
cd oracle && uv sync && uv run pytest -q

# Notes
cd notes/tex && latexmk -pdf main.tex
```

## 6. Ground rules (short version — full rules in `roadmap_v1.0.0.md`)

1. **No axioms, no `sorry` in `Core/`.** "Assumptions" are only definitions, satisfiable theorem
   hypotheses, or Mathlib theorems cited by name.
2. **Oracle before Lean.** Every claim is checked numerically (and mutants must fail) before a
   Lean statement is written.
3. **Spec before Lean, statement before proof.** Statements are locked; proofs may not change them.
4. **Miranda is a guide.** The OCR transcripts in `../references-transcripts/miranda_2003/` contain
   known errors; disagreements are recorded in `docs/WATCHLIST.md`.
5. **Notation contract.** ASCII machine layer for specs; typed indices (`Site`, `Mode`,
   `BosonIdx`, `Chirality`) in Lean.
6. **Human gates.** Each phase ends with a short gate packet reviewed by the human.

## 7. Tooling

- Lean 4 + Mathlib (pinned; see `docs/ENV.md`), VS Code/Antigravity extension `leanprover.lean4`.
- Python 3.12 + `uv` (numpy, scipy, sympy, pytest) for the oracle.
- TeX Live (`latexmk`, `pdflatex`, `bibtex`).
- Google Antigravity agents; Gemini models through the local LiteLLM proxy (`localhost:4000`).

## 8. Main reference

E. Miranda, *Introduction to Bosonization*, Braz. J. Phys. 33 (2003) — PDF in
`../reference-source/books/`, transcripts in `../references-transcripts/miranda_2003/`.
Umbral calculus on lattices: Dimakis–Müller-Hoissen–Striker (1996); Levi–Tempesta–Winternitz (2004).
Lattice AQFT / CAR nets: Bratteli–Robinson vol. 2; Araki's lattice CAR algebra.

