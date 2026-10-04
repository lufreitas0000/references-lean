# 1.1 Lattice, Band, and Index Types

## Definitions
- **Site**: The spatial lattice is a ring of $L$ sites, modeled as $\mathbb{Z}_L$.
- **Mode**: The momentum band is the set of integers $n$ such that $-L < 2n \le L$.
- **Chirality**: $\nu \in \{R, L\}$.

## Lean Implementation
- `Site L := ZMod L`
- `Mode L := { n : ℤ // -L < 2n ∧ 2n ≤ L }`
- `Chirality` is an inductive type.
