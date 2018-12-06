## module prob10_11
'''
Use the following decomposition to (a) compute the determinant and (b) solve using vec_B
(a) Determinant of A is product of diagonal down U matrix,
    det_A = (3) * (7.3333) * (3.6364) = 80.0004363
(b) See below:
'''
from matrix_mods import forward_sub, back_sub
def prob10_11():
    '''
    Use the following decomposition to (a) compute the determinant and (b) solve using vec_B
    (a) Determinant of A is product of diagonal down U matrix,
        det_A = (3) * (7.3333) * (3.6364) = 80.0004363
    (b) See below:
    '''
    L = [[ 1.0000, 0.0000, 0],
         [ 0.6667, 1.0000, 0],
         [-0.3333,-0.3636, 1]]
    U = [[ 3,-2.0000, 1.0000],
         [ 0, 7.3333,-4.6667],
         [ 0, 0.0000, 3.6364]]
    vec_B = [-10,
              44,
             -26]
    res_D = forward_sub(L, vec_B)
    sol = back_sub(U, res_D)
    for line in sol:
        print('{0: 1.2f} '.format(line))
prob10_11()