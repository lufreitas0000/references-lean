# Lean 4 & Mathlib Environment Specification

## System Information
- **OS**: Ubuntu 24.04 LTS (x86_64)
- **CPUs**: 12 cores
- **RAM**: ~47 GB
- **Project Root**: `/home/lucas/Projects/latex_notes/qed3-duality/references-lean`

## Toolchain & Versions
- **elan**: `4.2.4 (227caca13 2026-08-25)`
- **Lean toolchain**: `leanprover/lean4:v4.35.0-rc3`
- **Lean compiler**: `Lean (version 4.35.0-rc3, x86_64-unknown-linux-gnu, commit 470d5ce1400764999581fd26d5d72b00d990b0f4, Release)`
- **Lake build system**: `5.0.0-src+470d5ce (Lean version 4.35.0-rc3)`
- **Mathlib Tag**: `v4.35.0-rc3`
- **Mathlib Commit**: `c55e6e786f49471c72fbddbec5415808896aec1e`

## Setup Commands Used
1. **User-local elan installation (no sudo required)**:
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
   export PATH="$HOME/.elan/bin:$PATH"
   ```
2. **Project initialization and manifest generation via Lake template in `/tmp`**:
   ```bash
   cd /tmp
   lake +leanprover-community/mathlib4:lean-toolchain new bosonize math
   ```
3. **Project configuration**:
   - `lean-toolchain`: `leanprover/lean4:v4.35.0-rc3`
   - `lakefile.toml`: package name `bosonize`, lean_lib `Bosonize`, pinned to Mathlib tag `v4.35.0-rc3` with options `autoImplicit = false`, `relaxedAutoImplicit = false`.
   - `lake-manifest.json`: pinned Mathlib commit `c55e6e786f49471c72fbddbec5415808896aec1e`.
4. **Prebuilt olean cache retrieval**:
   ```bash
   lake exe cache get
   ```
   All precompiled Mathlib oleans downloaded/extracted without compiling Mathlib from source.
5. **Compilation**:
   ```bash
   lake build
   ```
   Build time: ~5 seconds (cached oleans).

## Verification & Smoke Tests
The project includes verification smoke tests demonstrating all project prerequisites:
- `Bosonize/Basic.lean`:
  - `sum_range_succ_smoke`: `∑ i ∈ range (n + 1), f i = (∑ i ∈ range n, f i) + f n` using `Finset.sum_range_succ`.
  - `polynomial_derivative_smoke`: `Polynomial.derivative (X ^ 2 : Polynomial ℚ) = 2 * X`.
  - `zmod_two_smoke`: `(x : ZMod 2) + x = 0`.
  - `fin_lt_smoke`: `(i : Fin n) → (i : ℕ) < n`.
  - `matrix_commutator_smoke`: Commutator $[ \sigma_x, \sigma_z ] = \begin{pmatrix} 0 & -2 \\ 2 & 0 \end{pmatrix}$ in `Matrix (Fin 2) (Fin 2) ℂ`.
- `Bosonize/Audit/AxiomCheck.lean`:
  - Axiom check on all smoke tests verifying dependency only on standard foundational Lean axioms (`propext`, `Classical.choice`, `Quot.sound`).
- `scripts/check_env.sh`:
  - Validates environment versions, Mathlib revision, builds project, and audits for any `sorry`, `admit`, or `axiom` occurrences (0 occurrences found).

## VS Code / Antigravity Extension Status
- Search path checked: `ls ~/.antigravity*/extensions ~/.vscode/extensions 2>/dev/null | grep -i lean`
- Result: Lean 4 extension is not currently pre-installed in extension directories.
- Recommended extension ID: `leanprover.lean4`.
