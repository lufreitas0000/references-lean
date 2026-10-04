# 1.2 Umbral Calculus Core

This section establishes the formal algebraic foundations of the discrete calculus used throughout the project. Let $R$ be a commutative ring. We define the calculus over two primary carriers (state spaces) of functions:
1. **Periodic fields**: Functions of the form $\text{Site}_L \to R$, where $\text{Site}_L$ represents a periodic domain of size $L$ (typically isomorphic to $\mathbb{Z}/L\mathbb{Z}$).
2. **Lattice functions**: Functions of the form $\mathbb{Z} \to R$, representing the unbounded integer lattice.

## Definitions: Discrete Operators

For a generic domain $S \in \{\mathbb{Z}, \text{Site}_L\}$, the space of functions $S \to R$ naturally forms an $R$-module and an $R$-algebra under pointwise operations. We define the following core linear operators in $\operatorname{End}_R(S \to R)$:

**Definition 1.2.1 (Shift Operator).** 
The shift operator $E$ is defined by its action on a function $f$:
$$ E(f)(x) := f(x + 1) $$
In the formalization, $E$ is constructed as a linear map (`LinearMap` / `Module.End R (S → R)`), and preserves pointwise multiplication, acting as an algebra endomorphism.

**Definition 1.2.2 (Forward and Backward Differences).** 
The forward difference operator $\Delta$ and backward difference operator $\nabla$ are defined in terms of $E$ and the identity operator $I$:
$$ \Delta := E - I \quad \implies \quad \Delta f(x) = f(x+1) - f(x) $$
$$ \nabla := I - E^{-1} \quad \implies \quad \nabla f(x) = f(x) - f(x-1) $$
On the space of lattice functions $\mathbb{Z} \to R$, the operator $\Delta$ corresponds directly to Mathlib's `fwdDiff` operator.

---

## Theorems: Umbral Algebra and Calculus

**Theorem 1.2.1 (Algebra Automorphism and Periodicity).**
The shift operator $E$ is an $R$-algebra automorphism of the function space $S \to R$. Furthermore, on the space of periodic fields $\text{Site}_L \to R$, $E$ acts cyclically such that:
$$ E^L = I $$

**Theorem 1.2.2 (Discrete Leibniz Rule).**
For any functions $f, g : S \to R$, the forward difference of their product satisfies the exact discrete Leibniz rule:
$$ \Delta(f \cdot g) = (\Delta f) \cdot g + (E f) \cdot (\Delta g) $$
*Proof.* Evaluated at $x$, we have $f(x+1)g(x+1) - f(x)g(x)$. Subtracting and adding $f(x+1)g(x)$ yields $(f(x+1)-f(x))g(x) + f(x+1)(g(x+1)-g(x))$, which is exactly $(\Delta f)(x)g(x) + (E f)(x)(\Delta g)(x)$.

**Theorem 1.2.3 (Discrete Fundamental Theorem of Calculus / Telescoping).**
On the periodic ring $\text{Site}_L \to R$, the sum of a forward difference identically vanishes:
$$ \sum_{x \in \text{Site}_L} \Delta f(x) = 0 $$
On the integer lattice $\mathbb{Z} \to R$, the sum over a bounded interval $[a, b) \subset \mathbb{Z}$ forms a telescoping series:
$$ \sum_{a \le x < b} \Delta f(x) = f(b) - f(a) $$

**Theorem 1.2.4 (Summation by Parts).**
On the periodic ring $\text{Site}_L \to R$, the forward difference $\Delta$ and backward difference $\nabla$ are negative adjoints of each other. For any $f, g : \text{Site}_L \to R$:
$$ \sum_{x \in \text{Site}_L} f(x) \Delta g(x) = - \sum_{x \in \text{Site}_L} \nabla f(x) g(x) $$
*(Equivalently, in terms of operators, $\Delta^\dagger = -\nabla$.)*

**Theorem 1.2.5 (Newton Expansion).**
The $n$-th composition of the shift operator can be expanded in terms of the forward difference operator via the binomial theorem (since $E = I + \Delta$ and $I$ commutes with $\Delta$):
$$ E^n = \sum_{k=0}^n \binom{n}{k} \Delta^k $$
This exactly mirrors the Mathlib identity `fwdDiff_iter_eq_sum_shift`.

**Theorem 1.2.6 (Difference of Falling Factorials).**
Let $X^{\underline{n}}$ denote the falling factorial polynomial (`descPochhammer R n`), defined as $X(X-1)\cdots(X-n+1)$. Viewing $X^{\underline{n}}$ as a polynomial in $R[X]$, and defining the polynomial difference operator as $\Delta p(X) := p(X+1) - p(X)$, we have:
$$ \Delta X^{\underline{n}} = n X^{\underline{n-1}} $$

**Theorem 1.2.7 (The Umbral Map).**
Let $\Phi : R[X] \to_l R[X]$ be the unique $R$-linear map (the "umbral map") defined on the standard basis by:
$$ \Phi(X^n) = X^{\underline{n}} $$
Let $D = \frac{d}{dX}$ be the formal derivative operator on $R[X]$. Then $\Phi$ acts as an intertwining operator between the formal derivative and the discrete difference operator:
$$ \Phi \circ D = \Delta \circ \Phi $$
*Remark: Because $D(X^n) = nX^{n-1}$ and $\Delta(X^{\underline{n}}) = nX^{\underline{n-1}}$ hold algebraically in $\mathbb{Z}$, the relation requires no division by integers. Therefore, this umbral property holds generally over any commutative ring $R$, without requiring $\mathbb{Q} \subseteq R$.*

**Theorem 1.2.8 (Umbral Heisenberg Pair).**
On the unbounded lattice space $\mathbb{Z} \to R$, define the linear operator $\beta \in \operatorname{End}_R(\mathbb{Z} \to R)$ by:
$$ (\beta f)(x) := x \cdot f(x-1) $$
The operators $\Delta$ and $\beta$ form an infinite-dimensional Heisenberg algebra pair, satisfying the canonical commutation relation:
$$ [\Delta, \beta] = \Delta \circ \beta - \beta \circ \Delta = I $$
*Proof.* 
Let $f : \mathbb{Z} \to R$. We evaluate $(\Delta \beta f)(x) - (\beta \Delta f)(x)$:
1. $(\beta f)(x) = x f(x-1)$
2. $(\Delta \beta f)(x) = (\beta f)(x+1) - (\beta f)(x) = (x+1)f(x) - x f(x-1)$
3. $(\beta \Delta f)(x) = x (\Delta f)(x-1) = x (f(x) - f(x-1)) = x f(x) - x f(x-1)$
Subtracting the two yields $((x+1) - x)f(x) = f(x)$, hence the commutator is the identity operator.

**Theorem 1.2.9 (Finite-Dimensional No-Go Theorem).**
Let $K$ be a field of characteristic $0$ ($\operatorname{char} K = 0$). There exist no finite-dimensional matrices $A, B \in \operatorname{Matrix}(n, n, K)$ with $n > 0$ such that:
$$ A B - B A = I $$
*Proof.* The trace of a commutator is identically zero: $\operatorname{Tr}(AB - BA) = \operatorname{Tr}(AB) - \operatorname{Tr}(BA) = 0$. However, the trace of the $n \times n$ identity matrix is $\operatorname{Tr}(I) = n$. This implies $n = 0$ in $K$. Since $\operatorname{char} K = 0$, this requires the ordinary integer $n$ to be $0$, which contradicts $n > 0$. 

*Motivation:* Theorem 1.2.9 demonstrates that the Heisenberg pair $(\Delta, \beta)$ from Theorem 1.2.8 cannot be realized in any finite-dimensional vector space. This fundamentally motivates the necessity of carefully managed infinite-dimensional spaces or strict computational "budgets" when implementing these umbral operations computationally.