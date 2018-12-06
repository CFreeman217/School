## module prob13_18b
'''
Test case for golden section search for local maxima
See also prob13_6a.py
'''
from golden import golden

def prob13_18b():
    '''
    Use the Golden section search to find the local minimum between 0 and the
    length of the beam within an error threshold of 1%
    '''
    w_0 = 2.5 # kN / cm
    length = 600 # cm
    I = 30000 # kN / cm^4
    E = 50000 # kN / cm^2
    func = lambda x : (w_0 / (120 * E * I * length)) * (-x**5 + 2*(length**2)*(x**3) - (length**4)*x)
    x_lower = 0
    x_upper = length
    er_max = 0.01
    x, y, error = golden(func, x_lower, x_upper, er_max, maxima=False)
    print('Golden Ratio Optimization Results:')
    print('Output "X" value : {:0.6f}'.format(x))
    print('Output "Y" value : {:0.6f}'.format(y))
    print('Estimated Error : {:0.6f}'.format(error))


prob13_18b()