## module example10_3
'''
Compute the matrix inverse of the following matrix
'''
from matrix_mods import mat_inverse
def example10_3():
    '''
    Compute the matrix inverse of the following matrix
    '''
    mat_A = [[3.0, -0.1, -0.2],
             [0.1,  7.0, -0.3],
             [0.3, -0.2, 10.0]]
    for line in zip(*mat_inverse(mat_A)):
        # FANCY FORMAT: {0:1.4E}
        #               0 is the index of the formatter tag
        #               : Separates the index number from the formatter
        #               1 Minimum digits to display before the decimal (space before to pad positives)
        #               . Decimal divider location
        #               4 Number of decimals to display
        #               E Use a capital E for scientific notation (f - float, e - lowercase e)
        print(['{0: 1.4E} '.format(k) for k in line])
example10_3()