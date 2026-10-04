import numpy as np

def check():
    L = 6
    zeta = np.exp(2j * np.pi / L)
    k = 1
    ek = np.array([zeta ** (k * x) for x in range(L)])
    E_ek = np.roll(ek, -1)
    Delta_ek = E_ek - ek
    
    expected = (zeta ** (-k) - 1) * ek
    return np.allclose(Delta_ek, expected)
