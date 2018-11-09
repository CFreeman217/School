## module bisection
'''
bisection(function, lower_guess, upper_guess, error_limit, max_iterations)
Uses bisection to find the root of the function. Inputs must straddle a root.
 - Example : prob5_16b.py
https://github.com/CFreeman217/NumericalMethods.git
'''

def bisection(funct, lowerguess, upperguess, er_limit=0.000001, max_iter=10):
    '''
    Numerical Methods - Roots of Functions

    Bisection Method:

    + As a bracketing method, this will always converge
    - Requires 2 initial conditions that bracket the root
    - Can be slow to converge
    - Does not find multiple or complex roots.
    Select two x-values that yield function outputs of opposite sign and
    this function performs bisection to find the root.

    funct : Function to evaluate the root
    lowerguess : Initial lower guess for x
    upperguess : Initial upper guess for x
    er_limit : Desired approximate error
    max_iter : Maximum number of iterations allowed
    '''
    # Find the point information from the function
    x_lower = lowerguess
    y_lower = funct(lowerguess)
    x_upper = upperguess
    y_upper = funct(upperguess)
    # Initialize an x guess
    x_guess = x_lower
    # While current error is outside the desired estimate and we are
    # within the iteration limit
    for iter_no in range(max_iter):
    # while c_error > er_limit and i_count < max_iter:
        # Store the previous value
        old_guess = x_guess
        # Generate a new guess for an x-value
        x_guess = (x_lower + x_upper) / 2
        # Create the corresponding y-value from the input function
        y_guess = funct(x_guess)
        # If the output from the guess and the lower bound are on the
        # same side of the x-axis.
        if y_guess * y_lower > 0:
            # The lower bound needs to be adjusted to the new guess
            x_lower = x_guess
            y_lower = y_guess
        elif y_guess * y_upper > 0:
            # Otherwise the other boundary needs to be adjusted
            x_upper = x_guess
            y_upper = y_guess
        else:
            # A true zero has been found
            break
        # Calculate the current Error for this iteration
        c_error = abs((x_guess - old_guess) / x_guess)
        if c_error < er_limit:
            break
    # Print the output
    print('Bisection Method Results : \n')
    print('Approximated Value : {}'.format(x_guess))
    print('Function Output : {}'.format(y_guess))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    # Returns the coordinates of the most recent guess
    return x_guess, y_guess

