# Notation Contract

## Symbol Table
| ASCII | Lean | Type | LaTeX | Miranda |
|---|---|---|---|---|
| `L` | `L` | `ℕ` | $L$ | $L$ |
| `Site` | `Site L` | `ZMod L` | $\mathbb{Z}_L$ | $x, y$ |
| `Mode` | `Mode L` | `ℤ`-subtype | $n, k$ | $k, q$ |
| `Chirality` | `Chirality` | `inductive` | $\nu \in \{R, L\}$ | $1, 2$ or $R, L$ |
| `dag(A)` | `star A` | `Module.End` | $A^\dagger$ | $A^\dagger$ |
| `nord(A)` | `nord A` | `Module.End` | $\nord{A}$ | $:A:$ |
| `E` | `shift` | `End` | $E$ | N/A |
| `Delta` | `fwdDiff`| `End` | $\Delta$ | $\partial_x$ |

## Rules
- **No bare superscripts:** Use `pow(x, n)`.
- **No nested colons.** Use `nord(A)`.
- **No bare slashes in ASCII:** Use typed fractions.
- All definitions are evaluated strictly. No `^` character in ````spec```` blocks.
