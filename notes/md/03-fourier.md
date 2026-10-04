# Finite Fourier

This section establishes the mathematically rigorous formalism for the Finite Fourier transform on the periodic 1D lattice $\mathbb{Z}_L$. Rather than relying exclusively on the analytic definition of roots of unity, the formalization heavily utilizes algebraic characterizations to ensure exact arithmetic and ease of reasoning in Lean.

## 1. Definitions

Throughout this section, let $L$ be a positive integer ($L > 0$), and let the spatial domain be the cyclic group $\mathbb{Z}_L = \mathbb{Z}/L\mathbb{Z}$. Let $R$ be a commutative ring (typically $\mathbb{C}$) equipped with an involution (complex conjugation).

**Definition 1.1 (Primitive Root of Unity).** \leanref{IsPrimitiveRoot}
We define $\zeta \in R$ abstractly as a primitive $L$-th root of unity. Analytically, this corresponds to $\zeta := \exp(2\pi i/L)$, but the Lean formalization abstracts this through the `IsPrimitiveRoot ζ L` predicate, which asserts that $L$ is the smallest positive integer such that $\zeta^L = 1$.

**Definition 1.2 (Plane Waves).** \leanref{planeWave}
For any momentum index $k \in \mathbb{Z}_L$, we define the plane wave basis function $e_k : \mathbb{Z}_L \to R$ by:
$$ e_k(x) := \zeta^{k x} $$
*Remark on well-definedness:* Since $k, x \in \mathbb{Z}_L$, their product $k x$ is naturally in $\mathbb{Z}_L$. The exponentiation $\zeta^{kx}$ is mathematically well-defined because $\zeta^L = 1$.

**Definition 1.3 (Discrete Fourier Transform).** \leanref{dft_matrix}
The Discrete Fourier Transform (DFT) matrix $U$ is defined by its components:
$$ U_{kx} := \frac{1}{\sqrt{L}} \zeta^{-kx} $$
The forward Discrete Fourier Transform of a function $f: \mathbb{Z}_L \to \mathbb{C}$ is:
$$ \hat{f}(k) = (Uf)_k = \frac{1}{\sqrt{L}} \sum_{x \in \mathbb{Z}_L} f(x) \zeta^{-kx} $$

## 2. Theorems

**Theorem 2.1 (Orthogonality of Plane Waves).** \leanref{planeWave_ortho}
The plane waves form an orthogonal basis under the standard summation over $\mathbb{Z}_L$. For any $k, k' \in \mathbb{Z}_L$:
$$ \sum_{x \in \mathbb{Z}_L} \zeta^{(k - k')x} = L \delta_{kk'} $$
By symmetry of the discrete Fourier kernel, the dual orthogonality sum over momenta also holds:
$$ \sum_{k \in \mathbb{Z}_L} \zeta^{(k - k')x} = L \delta_{xx'} $$

**Theorem 2.2 (Unitarity of the DFT).** \leanref{dft_unitary}
The DFT matrix $U$ is unitary. That is, $U U^\dagger = U^\dagger U = \mathbb{I}$, where $\mathbb{I}$ is the identity operator on $\ell^2(\mathbb{Z}_L)$. Equivalently, the inverse transform is given by:
$$ f(x) = \frac{1}{\sqrt{L}} \sum_{k \in \mathbb{Z}_L} \hat{f}(k) \zeta^{kx} $$

**Theorem 2.3 (Difference Operators in Momentum Space).** \leanref{fwd_diff_planeWave}, \leanref{bwd_diff_planeWave}
The finite difference operators $\Delta$ (forward) and $\nabla$ (backward) act diagonally on the plane wave basis. Specifically:
$$ \Delta e_k = (\zeta^k - 1) e_k $$
$$ \nabla e_k = (1 - \zeta^{-k}) e_k $$

## 3. Proofs and Discussions

### 3.1 Resolving the Sign Convention Hazard
**Hazard Note:** There is a known divergence in the literature regarding the sign of the exponent in the Fourier transform, specifically noted between Miranda equations (8) and (9) (W-15). 
*   **Forward Transform (Miranda 8):** Uses the negative exponent $\zeta^{-kx}$.
*   **Inverse Transform (Miranda 9):** Uses the positive exponent $\zeta^{kx}$.

Our formalization acts as the "oracle" to strictly enforce this convention. By establishing $U_{kx} \propto \zeta^{-kx}$ and $(U^\dagger)_{xk} \propto \zeta^{kx}$, we maintain consistency with standard quantum mechanical momentum-space conventions (where $p \cdot x$ appears with a negative sign in the transform). All subsequent proofs of unitarity and convolution theorems must rigorously adhere to these signs to avoid off-by-one errors or unintended complex conjugations.

### 3.2 Proof of Orthogonality (App. A.1 finite sums)
The proof of Theorem 2.1 relies on the geometric series for primitive roots. Let $m = k - k' \pmod L$.
*   **Case $m = 0$ ($k = k'$):** $\zeta^{mx} = \zeta^0 = 1$. The sum is $\sum_{x=0}^{L-1} 1 = L$.
*   **Case $m \neq 0$ ($k \neq k'$):** Since $\zeta$ is a primitive $L$-th root, $\zeta^m \neq 1$. Applying the finite geometric series formula:
    $$ \sum_{x=0}^{L-1} (\zeta^m)^x = \frac{(\zeta^m)^L - 1}{\zeta^m - 1} = \frac{(\zeta^L)^m - 1}{\zeta^m - 1} = \frac{1^m - 1}{\zeta^m - 1} = 0 $$
This exact algebraic vanishing avoids floating-point inaccuracies and is handled cleanly in Lean via the `geom_sum` and `IsPrimitiveRoot` APIs.

### 3.3 Proof of DFT Unitarity
To verify $U U^\dagger = \mathbb{I}$:
$$ (U U^\dagger)_{k k'} = \sum_{x \in \mathbb{Z}_L} U_{kx} (U^\dagger)_{xk'} = \sum_{x \in \mathbb{Z}_L} \left( \frac{1}{\sqrt{L}} \zeta^{-kx} \right) \left( \frac{1}{\sqrt{L}} \overline{\zeta^{-k'x}} \right) $$
Since $\zeta = \exp(2\pi i/L)$, its complex conjugate is $\zeta^{-1}$. Thus, $\overline{\zeta^{-k'x}} = \zeta^{k'x}$.
$$ (U U^\dagger)_{k k'} = \frac{1}{L} \sum_{x \in \mathbb{Z}_L} \zeta^{(k' - k)x} $$
By Theorem 2.1, this sum evaluates to $L \delta_{k k'}$, yielding:
$$ (U U^\dagger)_{k k'} = \delta_{k k'} $$
confirming $U$ is unitary.

### 3.4 Proof of Diagonal Difference Operators (Miranda 14')
The difference operators act on spatial indices. For the forward difference $\Delta f(x) = f(x+1) - f(x)$, we apply it to $e_k(x)$:
$$ \Delta e_k(x) = \zeta^{k(x+1)} - \zeta^{kx} = \zeta^{kx} \zeta^k - \zeta^{kx} = (\zeta^k - 1) \zeta^{kx} = (\zeta^k - 1) e_k(x) $$
Similarly, for the backward difference $\nabla f(x) = f(x) - f(x-1)$:
$$ \nabla e_k(x) = \zeta^{kx} - \zeta^{k(x-1)} = \zeta^{kx} - \zeta^{kx} \zeta^{-k} = (1 - \zeta^{-k}) \zeta^{kx} = (1 - \zeta^{-k}) e_k(x) $$
This confirms that the plane waves $e_k$ are the eigenfunctions of the discrete translation and difference operators on the lattice, with eigenvalues $(\zeta^k - 1)$ and $(1 - \zeta^{-k})$, corresponding to Miranda's equation (14').