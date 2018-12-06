## module example4_4
''' Test for Centered finite divided difference first derivative formulas using known function and list of data points.'''

from div_dif_deriv import cfdd_1deriv, num_1deriv

def ex4_4():
    '''
    Test case for cfdd_1deriv
    Original goal was to evaluate derivative at center point in vector. Num_1deriv runs forward or backward finite difference
    at the edges to generate a derivative estimate vector that is the same size as the input values. Correct solution is shown.
    -0.9125
    [0.2375000000000007, -0.2875, -0.9125, -2.2375000000000003, -3.8125000000000004]
    '''
    func = lambda x : -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.25
    val = 0.5
    hgt = 0.5
    x_list = [(i*0.5 - 0.5) for i in range(5)]
    y_list = [func(i) for i in x_list]
    print(cfdd_1deriv(func, val, hgt))
    print(num_1deriv(x_list, y_list))

ex4_4()