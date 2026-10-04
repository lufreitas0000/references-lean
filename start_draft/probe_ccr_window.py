import numpy as np, math, scipy.sparse as sp
L = 12
modes = list(range(-L//2+1, L//2+1)); D=len(modes); dim=2**D
I2 = sp.identity(2,format='csr'); Z = sp.diags([1.,-1.]).tocsr(); a = sp.csr_matrix(np.array([[0,1],[0,0]],float))
def kron_all(ms):
    out = ms[0]
    for m in ms[1:]: out = sp.kron(out,m,format='csr')
    return out
c = {n: kron_all([Z]*i+[a]+[I2]*(D-i-1)) for i,n in enumerate(modes)}
cd = {n: c[n].T.tocsr() for n in modes}
def rho(m):
    R = sp.csr_matrix((dim,dim))
    for n in modes:
        if (n+m) in c: R = R + cd[n+m]@c[n]
    return R
bm = {m: rho(-m)/math.sqrt(m) for m in range(1,L//2+1)}
bd = {m: bm[m].T.tocsr() for m in bm}
# energies
idx = np.arange(dim)
bits = ((idx[:,None] >> (D-1-np.arange(D))[None,:]) & 1)
mv = np.array(modes)
Ncount = bits.sum(1) - L//2
P = bits@mv - sum(n for n in modes if n<=0)
es = P - Ncount*(Ncount+1)//2
assert es.min()==0
def budget_vecs(K,Nmax):
    sel = np.where((es<=K)&(np.abs(Ncount)<=Nmax))[0]
    V = sp.csr_matrix((np.ones(len(sel)),(sel,np.arange(len(sel)))),shape=(dim,len(sel)))
    return V
res = {}
for Nmax in [0,1,2]:
  for K in range(0,5):
    V = budget_vecs(K,Nmax)
    # find largest Q such that CCR holds for all m,m'<=Q on the budget
    best = 0
    for Q in range(1,L//2+1):
        ok=True
        for m in range(1,Q+1):
            for mp in range(1,Q+1):
                comm = bm[m]@bd[mp] - bd[mp]@bm[m]
                tgt = (m==mp)*sp.identity(dim,format='csr')
                if abs((comm-tgt)@V).max() > 1e-9: ok=False;break
            if not ok:break
        if ok: best=Q
        else: break
    res[(Nmax,K)] = best
    print("L=%d  |N|<=%d  K=%d : largest Q with exact CCR on budget = %d   (L/2-K-|N| = %d)"%(L,Nmax,K,best,L//2-K-Nmax))
