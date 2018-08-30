import sympy as sp

def prob2_7b():
    s = sp.symbols('s')
    t = sp.symbols('t', positive=True)
    G = (s**3 + 4*s**2 + 2*s + 6) / ((s+8)*(s**2 + 8*s + 3)*(s**2 + 5*s + 7))
    # G = 1/((s + 3)**2)
    sp.pprint(G)
    sol = sp.inverse_laplace_transform(G, s, t)
    sp.pprint(sol)

prob2_7b()