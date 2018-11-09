## module prob10_9
'''
Solve the system of equations using LU Decomposition and back substitution
'''
from matrix_mods import lu_decomp, forward_sub, back_sub
from NumericalMethods import gauss_elim
# def prob10_9():
#     '''
#     Solve the system of equations using LU Decomposition and back substitution
#     '''
#     mat_A = [[ 3, -2, 1],
#              [ 2,  6,-4],
#              [-1, -2, 5]]
#     vec_B = [-10,
#               44,
#              -26]
#     lowr, upr = lu_decomp(mat_A)
#     print('Lower Matrix : ')
#     for line in lowr:
#         print(line)
#     print('Upper Matrix : ')
#     for line in upr:
#         print(line)
#     res_D = forward_sub(lowr,vec_B)
#     print('Forward Vector : ')
#     for line in res_D:
#         print(line)
#     sol = back_sub(upr,res_D)
#     print('Solution : ')
#     for line in sol:
#         print(line)

def ex2_12():
    matrix_A = [[ 2,-2, 6],
             [-2, 4, 3],
             [-1, 8, 4]]

    vec_B = [16,
             0,
            -1]

    # sol = gauss_elim(matrix_A, vec_B)
    # print(sol)
    print(matrix_A)
    lowr, upr = lu_decomp(matrix_A)
    print('Lower Matrix : ')
    for line in lowr:
        print(line)
    print('Upper Matrix : ')
    for line in upr:
        print(line)
    res_D = forward_sub(lowr,vec_B)
    print('Forward Vector : ')
    for line in res_D:
        print(line)
    sol = back_sub(upr,res_D)
    print('Solution : ')
    for line in sol:
        print(line)
ex2_12()
# prob10_9()