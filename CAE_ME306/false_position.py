## module false_position
'''
false_position(funct, lowerguess, upperguess, er_limit=0, max_iter=10)
    Numerical Methods - Roots of functions

    False Position Method:

    Takes a function with lower and upper bounds to find the root
    after an iteration limit with error approximation using false
    position.

    funct : Function to evaluate the root
    lowerguess : Initial lower guess for x
    upperguess : Initial upper guess for x
    max_iter : Maximum number of iterations allowed

    see prob5_17.py

https://github.com/CFreeman217/NumericalMethods.git
'''


def false_position(funct, lowerguess, upperguess, er_limit=0.00001, max_iter=10):
    '''
    Numerical Methods - Roots of functions

    False Position Method:

    Takes a function with lower and upper bounds to find the root
    after an iteration limit with error approximation using false
    position.

    funct : Function to evaluate the root
    lowerguess : Initial lower guess for x
    upperguess : Initial upper guess for x
    max_iter : Maximum number of iterations allowed
    '''
    # Find the point information from the function
    x_lower = lowerguess
    y_lower = funct(lowerguess)
    x_upper = upperguess
    y_upper = funct(upperguess)
    # Initialize a guess
    x_guess = 0
    # Initialize iteration counter
    for iter_no in range(max_iter):

        # Store the previous value
        old_guess = x_guess
        # Generate a new guess for the root
        x_guess = x_upper - (y_upper * (x_lower - x_upper))/(y_lower - y_upper)
        # Find the function output from the new guess
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
        # Calculate the current estimated error on this iteration
        c_error = abs((x_guess - old_guess) / x_guess)
        if c_error < er_limit:
            # The calculated error has dropped below the required threshold
            break
    # Print output
    print('False Position Method Results : \n')
    print('Approximated Value : {}'.format(x_guess))
    print('Function Output : {}'.format(y_guess))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    # Returns the coordinates of the most recent guess
    return x_guess, y_guess

