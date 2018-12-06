
def root_approx(in_value, er_limit, max_iter):
    '''
    Numerical Methods - Function Value Approximation

    Estimates the square root of the input value down to an error limit or
    the maximum number of iterations.

    in_value : The number we want to estimate the square root for
    er_limit : The estimated error threshold
    max_iter : The maximum number of iterations through the for loop
    '''
    # Initialize iteration counter
    i_count = 0
    # Current error is set at 100%
    c_error = 1.0
    # Initialize an initial guess for the square root
    x_guess = in_value
    # While current error is outside the desired estimate and we are
    # within the iteration limit
    while c_error > er_limit and i_count < max_iter:
        # Store the previous value
        old_guess = x_guess
        # Generate a new guess for an x-value
        x_guess = (x_guess + in_value/x_guess)/2
        # Cycle the iterator
        i_count += 1
        # Only update approximate error if estimate is not zero
        if x_guess != 0:
            # Calculate the current Error for this iteration
            c_error = abs((x_guess - old_guess) / x_guess)
    print('Square root of : {}\nApproximated as : {}\nEstimated Error : {}'.format(in_value, x_guess, c_error))
    return x_guess

def cos_approx(in_value, sig_figs):
    '''
    Numerical Methods - Function Value Approximation

    Estimates the value of cosine at the input value to the specified number of
    significant figures using the taylor expansion.

    in_value : The number we would like to evaluate for cosine
    sig_figs : The number of significant figures for precision
    '''
    from math import factorial, cos
    # Generate the termination criteria in percent
    er_limit = 0.5*10**(2-sig_figs)
    # Current error is set at 100%
    c_error = 1.0
    # Initialize iteration counter at 2 to use as exponent in series
    i_count = 2
    # Multiplier for switching sign on each iteration
    mult = -1
    # Initialize an initial value for the first term in the Maclaurin Series
    c_term = 1
    # While current error is outside the required threshold
    while c_error > er_limit:
        # Store the previous term value
        old_term = c_term
        # Generate the next term in the series
        c_term += mult*in_value**i_count/factorial(i_count)
        # Cycle the multiplier
        mult *= -1
        # Cycle the iterator
        i_count += 2
        if c_term != 0:
            # Update the current error estimate
            c_error = abs((c_term - old_term) / c_term)
    # Return the approximation and the true value
    print('Cosine evaluated at : {}\nApproximation Calculated : {}\nTrue Value : {}'.format(in_value, c_term, cos(in_value)))
    return c_term, cos(in_value)

prob3_13 = root_approx(81, 0.0001, 20)

from math import pi

prob4_2, actual = cos_approx(pi/3, 2)