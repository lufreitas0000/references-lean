from fock import FockSpace
import numpy as np

def check():
    fock = FockSpace(6)
    m = 1
    comm = fock.rho(-m) @ fock.rho(m) - fock.rho(m) @ fock.rho(-m)
    
    vac = fock.vacuum
    diff = comm @ vac
    return np.linalg.norm(diff) < 1e-8
