## module example11_3
'''
Use the Gauss-Seidel method to obtain the solution of the system
3.0 * x_1 - 0.1 * x_2 - 0.2 * x_3 = 7.85
0.1 * x_1 + 7.0 * x_2 - 0.3 * x_3 = -19.3
0.3 * x_1 - 0.2 * x_2 +  10 * x_3 = 71.4

x_1 = 3
x_2 = -2.5
x_3 = 7
'''
from gauss_seidel import gauss_seidel

def example11_3():
    '''
    RESULTS:
    [2.9999999980555687, -2.500000000456044, 7.000000000049213]
    '''
    mat_A = [[3.0,-0.1,-0.2],
             [0.1, 7.0,-0.3],
             [0.3,-0.2, 10]]
    vec_b = [ 7.85,
             -19.3,
              71.4]

    ans = gauss_seidel(mat_A, vec_b)
    print(ans)
example11_3()