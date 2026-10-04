import numpy as np
import scipy.sparse as sp
from fock import FockSpace

def check():
    fock = FockSpace(6)
    Id = sp.identity(fock.dim, format="csr", dtype=float)
    
    m = 1
    comm = fock.rho(-m) @ fock.rho(m) - fock.rho(m) @ fock.rho(-m)
    tgt = -m * Id
    
    vac = fock.vacuum
    diff = (comm - tgt) @ vac
    return np.linalg.norm(diff) < 1e-8
