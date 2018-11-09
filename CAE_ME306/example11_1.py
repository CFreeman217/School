## module example11_1
'''
Test case for thomas algorithm for solving tridiagonal systems of equations
'''
from thomas import thomas
def example11_1():
    '''
    Solve the following tridiagonal system with the thomas algorithm
    '''
    # The primary diagonal
    in_f = [2.04, 2.04, 2.04, 2.04]
    # Bottom coefficients
    in_e = [-1, -1, -1]
    # Top coefficients
    in_g = [-1, -1, -1]
    # known vector
    in_b = [40.8, 0.8, 0.8, 200.8]
    ans = thomas(in_f, in_e, in_g, in_b)
    print(ans)
example11_1()