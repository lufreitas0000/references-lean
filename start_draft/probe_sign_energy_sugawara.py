import numpy as np, itertools, math
np.set_printoptions(linewidth=200)

def build(L):
    modes = list(range(-L//2+1, L//2+1))      # n in (-L/2, L/2]
    D = len(modes)
    I2 = np.eye(2); Z = np.diag([1.,-1.]); a = np.array([[0,1],[0,0]],float)  # annihilation: |1>->|0>, basis (|0>,|1>)
    # basis ordering: index0=empty, index1=occupied ; a|1>=|0>
    def kron_all(ms):
        out = ms[0]
        for m in ms[1:]: out = np.kron(out, m)
        return out
    c = {}
    for i,n in enumerate(modes):
        ms = [Z]*i + [a] + [I2]*(D-i-1)
        c[n] = kron_all(ms)
    return modes, c

def occ_state(modes, occ):
    # occ: set of occupied n
    v = np.array([1.])
    for n in modes:
        v = np.kron(v, np.array([0.,1.]) if n in occ else np.array([1.,0.]))
    return v

L = 8
modes, c = build(L)
D = len(modes); dim = 2**D
cd = {n: c[n].T for n in modes}
# check CAR
for n in modes:
    for p in modes:
        ac = c[n]@cd[p] + cd[p]@c[n]
        assert np.allclose(ac, (n==p)*np.eye(dim))
        assert np.allclose(c[n]@c[p]+c[p]@c[n], 0)
print("CAR ok, dim", dim)

def rho(m):
    R = np.zeros((dim,dim))
    for n in modes:
        if (n+m) in c:
            R += cd[n+m]@c[n]
    return R

vac = occ_state(modes, {n for n in modes if n<=0})
Nop = sum(cd[n]@c[n] for n in modes) - (L//2)*np.eye(dim)
# 1. Eq (45)-style sign
for m in [1,2,3]:
    comm = rho(m)@rho(-m) - rho(-m)@rho(m)
    print("m=%d  <vac|[rho(m),rho(-m)]|vac> = %.3f"%(m, vac@comm@vac))

# energy of basis states
def basis_occ(idx):
    bits = [(idx >> (D-1-i)) & 1 for i in range(D)]
    return {modes[i] for i in range(D) if bits[i]}
def energy(occ):
    N = len(occ) - L//2
    P = sum(occ) - sum(n for n in modes if n<=0)
    return P - N*(N+1)//2, N
es = []; Ns=[]
for idx in range(dim):
    e,N = energy(basis_occ(idx)); es.append(e); Ns.append(N)
es=np.array(es); Ns=np.array(Ns)
print("min energy over all states:", es.min(), "(should be >=0)")
# deep hole: remove n=-d from vacuum
for d in range(0,4):
    occ = {n for n in modes if n<=0}-{-d}
    print("single hole at n=-%d : sector N=%d energy e=%d"%(d,*reversed(energy(occ))) )

# 2. Budget exactness of CCR and Sugawara
def budget_proj(K, Nmax):
    mask = (es<=K)&(np.abs(Ns)<=Nmax)
    return mask
def b(m): return rho(-m)/math.sqrt(m)
H0 = sum(n*(cd[n]@c[n]) for n in modes) - sum(n for n in modes if n<=0)*np.eye(dim)   # sum n :n_n:  (momentum operator P)
def check(K,Nmax):
    mask = budget_proj(K,Nmax)
    idxs = np.where(mask)[0]
    V = np.eye(dim)[:,idxs]       # columns = budget basis vectors
    worst_ccr = 0; 
    for m in range(1,4):
        for mp in range(1,4):
            if m+K>L: continue
            comm = b(m)@b(mp).T - b(mp).T@b(m)
            tgt = (m==mp)*np.eye(dim)
            worst_ccr = max(worst_ccr, np.abs((comm-tgt)@V).max())
    S = sum(m*(b(m).T@b(m)) for m in range(1,L//2))  # sum m b^dag b
    Pop = H0 - (Nop@(Nop+np.eye(dim)))/2
    sug = np.abs((Pop - S)@V).max()
    return worst_ccr, sug
for K in range(0,5):
    for Nmax in [0,1]:
        print("K=%d |N|<=%d : max CCR violation=%.2e  max Sugawara violation=%.2e  (budget dim %d)"%(K,Nmax,*check(K,Nmax), budget_proj(K,Nmax).sum()))
