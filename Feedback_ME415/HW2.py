

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
    from scipy.signal import residue, zpk2tf, TransferFunction
    from numpy import roots

    num = [-5, 70]
    den = [0, -45, -55, (roots([1, 7, 110])), (roots([1, 6, 95]))]

    num_tf, den_tf = zpk2tf(num, den, 10000)
    G_tf = transferFunction(num_tf, den_tf)
