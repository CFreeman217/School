## module example_matmult
'''
Test case for matrix multiplication
'''
from matrix_mods import mat_mult
a = [[34,1,77],
     [2,14,8],
     [3,17,11]]
b = [[6,8,1],
     [9,27,5],
     [2,43,31]]

c = [[1,2,3],
     [4,5,6]]

d = [[7,8],
     [9,10],
     [11,12]]

e = [[1,6],
     [3,10],
     [7,4]]

f = [[1,3],
     [.5,2]]
print(mat_mult(c,d))