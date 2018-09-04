

def prob2_7b():
    import sympy as sp
    s = sp.symbols('s')
    t = sp.symbols('t', positive=True)
    # G = ((s**2 + 3*s + 10)*(s + 5))/((s + 3)*(s + 4)*(s**2 + 2*s + 100))
    G = (s**3 + 4*s**2 + 2*s + 6) / ((s+8)*(s**2 + 8*s + 3)*(s**2 + 5*s + 7))
    sol = sp.inverse_laplace_transform(G, s, t)
    sp.pprint(G)
    sp.pprint(sol)

# prob2_7b()

def prob2_15():
    import numpy as np
    from scipy.signal import residue, zpk2tf, TransferFunction
    from numpy import roots

    num = [-5, 70]
    rp1 = (roots([1, 7, 110]).T.conj())
    rp2 = (roots([1, 6, 95]).T.conj())
    print(rp1[0])
    # den = [0, -45, -55, rp1[0][0], rp1[0][1], rp2[0][0], rp2[0][1]]
    # print(num)
    # print(den)
    # num_tf, den_tf = zpk2tf(np.atleast_2d(num).T.conj(), np.atleast_2d(den).T.conj(), 10000)
    # G_tf = transferFunction(num_tf, den_tf)
    # print(G_tf)
prob2_15()