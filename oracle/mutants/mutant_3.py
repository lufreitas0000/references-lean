from fock import FockSpace
import numpy as np

def check():
    fock = FockSpace(4)
    vac = fock.vacuum
    n_0 = fock.n_op[0]
    val = vac @ (n_0 @ vac)
    # Returns True if n=0 is empty (which means n<0 filled, not n<=0)
    return float(val) < 1e-8
