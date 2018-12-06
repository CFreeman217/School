## module muller_method
'''
Numerical Methods - Muller Method

This method takes three guesses around a local root and draws a parabola through
the three points. Then, using the quadratic formula, roots are found. This method
can be used to find complex roots. This method is slightly slower than the
Newton-Raphson method. The three function outputs cannot be colinear or else a
parabola cannot be fit to the points.

funct : The function we are trying to find the root for
guess1 : First guess for initializing a lower bound on drawing a parabola
guess2 : Second guess should be between guesses 1 and 3
guess3 : Third guess to initiate the algorithm
er_limit : Estimated error threshold (optional, default is 0.0001)
max_iter : Maximum number of iterations (optional, default is 10)

See example7_2.py
    prob7_3a.py
    prob7_3b.py
    prob7_11.py
'''

def muller_method(funct, guess1, guess2, guess3, er_limit=0.00001, max_iter=10):
    '''
    Numerical Methods - Muller Method

    This method takes three guesses around a local root and draws a parabola through
    the three points. Then, using the quadratic formula, roots are found. This method
    can be used to find complex roots. This method is slightly slower than the
    Newton-Raphson method. The three function outputs cannot be colinear or else a
    parabola cannot be fit to the points.

    funct : The function we are trying to find the root for
    guess1 : First guess for initializing a lower bound on drawing a parabola
    guess2 : Second guess should be between guesses 1 and 3
    guess3 : Third guess to initiate the algorithm
    er_limit : Estimated error threshold (optional, default is 0.0001)
    max_iter : Maximum number of iterations (optional, default is 10)
    '''
    # The python equivalent for fzero in matlab. not standard
    from scipy.optimize import fsolve
    # The complex math library can handle negative square roots. Assign this
    # functionality for the usage : csqrt(-1) = 1j
    from cmath import sqrt as csqrt
    # Assign the guesses to locally defined variables
    x_guess1 = guess1
    x_guess2 = guess2
    x_guess3 = guess3
    for iter_no in range(max_iter):
        # generate the outputs for the function
        y_guess1 = funct(x_guess1)
        y_guess2 = funct(x_guess2)
        y_guess3 = funct(x_guess3)
        # Find the horizontal spacing between the three input guesses
        distance_a = x_guess2 - x_guess1
        distance_b = x_guess3 - x_guess2
        # Get the slope for lines passing through the points
        del_a = ((y_guess2 - y_guess1)/distance_a)
        del_b = ((y_guess3 - y_guess2)/distance_b)
        # Produce coefficients to generate a parabola through the
        # three points
        parab_a = (del_b - del_a)/(distance_b + distance_a)
        parab_b = (parab_a * distance_b) + del_b
        # Square root of discriminant
        root_disc = csqrt(parab_b**2 - 4*parab_a*y_guess3)
        # Make sure that the root is not complex
        if root_disc.imag == 0:
            # Generate a new guess for x and find the error
            x_guess4 = x_guess3 - (2*y_guess3)/(parab_b + root_disc.real)
            # Calculate the current error
            c_error = abs((x_guess4 - x_guess3)/ x_guess4)
            # Check the error
            if c_error < er_limit:
                break
            else:
                # If the current error is outside the threshold, sequence
                # the variables ahead and get ready to iterate again
                x_guess1 = x_guess2
                x_guess2 = x_guess3
                x_guess3 = x_guess4
        else:
            print('Imaginary Root for discriminant')
            # future work here
            break


    print('\nMuller Method Results : \n')
    print('Approximated Value : {}'.format(x_guess3))
    print('Function Output : {}'.format(y_guess3))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    print('SciPy fsolve output : {}'.format(fsolve(funct, x_guess1)))

