## module thomas
'''
Thomas Algorithm for solving tridiagonal systems

See example11_1.py
    prob11_3.py
'''



def thomas(f_diag, e_diag, g_diag, b_vec):
    '''
    Numerical Methods : Thomas Algorithm

    A computationally lightweight method for solving tridiagonal matrices

    [ f(0) g(0)                           ][ x(0) ]   [ b(0) ]
    [ e(1) f(1) g(1)                      ][ x(1) ]   [ b(1) ]
    [      e(2) f(2) g(2)                 ][ x(2) ]   [ b(2) ]
    [            ...   ...   ...          ][ ...  ] = [ ...  ]
    [                e(n-1) f(n-1) g(n-1) ][x(n-1)]   [b(n-1)]
    [                        e(n)   f(n)  ][ x(n) ]   [ b(n) ]

    f_diag = Primary diagonal
    e_diag = Bottom coefficients - begins with a zero
    g_diag = Top coefficients - ends with a zero
    b_vec = Known vector quantities

    Returns a list of solved values
    '''
    # Get the number of values to find
    n = len(b_vec)
    # Append zero to beginning of e matrix
    e_diag = [0] + e_diag
    # Append zero to end of g matrix
    g_diag.append(0)
    # Initiate a solution vector full of zeros
    sol_vec = [0 for i in range(n)]
    # Decomposition
    for k in range(1,n):
        e_diag[k] /= f_diag[k-1]
        f_diag[k] -= e_diag[k] * g_diag[k-1]
    # Forward substitution
    for k in range(1,n):
        b_vec[k] -= e_diag[k] * b_vec[k-1]
    # Back substitution
    sol_vec[-1] = b_vec[-1]/f_diag[-1]
    for k in range(n-2,-1,-1):
        sol_vec[k] = (b_vec[k] - g_diag[k] * sol_vec[k+1]) / f_diag[k]
    return sol_vec

