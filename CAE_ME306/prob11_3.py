## module prob11_3.py
'''
Test case for thomas algorithm for solving tridiagonal systems of equations
'''
from thomas import thomas
def prob11_3():
    '''
    The following tridiagonal system must be solved as part of a larger algorithm
    (Crank-Nicholson) for solving partial differential equations. Use the Thomas
    algorithm to obtain a solution
    '''
    # The primary diagonal
    in_f = [2.01475] * 4
    # Bottom coefficients
    in_e = [-0.020875] * 3
    # Top coefficients
    in_g = in_e
    # known vector
    in_b = [4.175, 0, 0, 2.0875]
    ans = thomas(in_f, in_e, in_g, in_b)
    print(ans)
prob11_3()

def final_sample():
    side1 = 240 # Temperature of left side of rod (known)
    side2 = 150 # Temperature of right side of rod (known)
    n_segments = 10 # Slices for the integral
    # Matrix length
    mat_size = n_segments - 1
    # Primary diagonal value
    prim_diag = 2.15
    # Top and bottom vectors
    top_bot = 1
    # The primary diagonal
    in_f = [prim_diag] * mat_size
    # Bottom coefficients
    in_e = [top_bot] * (mat_size-1)
    # Top coefficients
    in_g = in_e
    # known vector
    in_b = np.zeros(mat_size)
    # Set the boundary conditions
    in_b[0] = side1
    in_b[-1] = side2
    fin_dif = thomas(in_f, in_e, in_g, in_b)