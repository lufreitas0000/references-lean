# ADR 13: Multi-Agent Topology and Boundary Constraints

## Decision
To prevent context bloat, logical circularity, and adversarial compiler bypasses in Lean 4, the multi-agent system is strictly partitioned into orthogonal color-coded teams (Yellow, Blue, Red, Purple, White).

## Roles and I/O
* **Yellow Team (Top-Down Architects):** Maps physical concepts (AQFT, Umbral Calculus) to interfaces. Generates definitions, axioms, and `sorry`-locked Lean signatures (Stubs).
* **Blue Team (Bottom-Up Constructors):** Maps interfaces to implementations. Generates constructive Lean proofs and Python Oracle logic.
* **Red Team (Adversarial Validators):** Audits and attempts to break the code. Injects mutations into the Oracle, hunts for vacuous truths in Lean, and triggers anti-cheat guards.
* **Purple Team (Integrators):** Translates state. Analyzes Red/Blue deadlocks and generates actionable prompts (lemma decompositions) for Yellow/Blue.
* **White Team (Orchestrator):** Human/Harness control plane. Allocates API budgets and enforces Dependency Inversion.

## Consequences
Agents cannot bypass their constraints. Blue cannot rewrite Yellow's stubs; it must fail and yield to Purple.
