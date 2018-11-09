## module prob13_6a
'''
Test case for the golden section search for unconstrained optimization
See also prob13_18b.py
'''
from golden import golden
def prob13_6a():
    '''
    Use the Golden section search to find the local maximum between -2 and 4
    within an error threshold of 1%
    '''
    func = lambda x : 4*x - 1.8*x**2 + 1.2*x**3 - 0.3*x**4
    x_lower = -2
    x_upper = 4
    er_max = 0.01
    x, y, error = golden(func, x_lower, x_upper, er_max)
    print('Golden Ratio Optimization Results:')
    print('Output "X" value : {:0.6f}'.format(x))
    print('Output "Y" value : {:0.6f}'.format(y))
    print('Estimated Error : {:0.6f}'.format(error))
prob13_6a()