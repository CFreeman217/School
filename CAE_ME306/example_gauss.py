## module example_gauss
''' test case for gauss elimination module'''
from gauss_elimination import naive_gauss_pivot
def example():
    # Results : [1.0, 0.9999999999999999, 1.0]
    c_matrix = [[1,2,-1],\
                [5,2,2],\
                [-3,5,-1]]
    e_elem = [2,9,1]
    naive_gauss_pivot(c_matrix, e_elem)

example()