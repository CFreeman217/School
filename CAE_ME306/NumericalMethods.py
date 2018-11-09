## module NumericalMethods
'''
Numerical Methods v1.0

Created 3 May, 2018 by Clay Freeman

email: freeman.clayton@gmail.com

Citations :

S. C. Chapra and R. P. Canale, Numerical Methods for Engineers, 7th Edition ed., New York, New York: McGraw-Hill, 2015.
J. Kiusalaas, Numerical Methods in Engineering with Python 3, New York, New York: Cambridge University Press, 2013.

Roots of Functions :
 - Bisection
 - False position
 - Muller method
 - Newton-Raphson method
 - Seacant method

Systems of Equations :
 - Gauss elimination
 - Gauss-Seidel method
 - Matrix inversion
 - Doolittle matrix pivoting
 - LU Decomp
 - Forward substitution
 - Back substitution
 - Thomas algorithm for tridiagonal systems

Optimization :
 - Golden section
 - Newton-Raphson optimization

Differentiation :
 - First derivative of function
 - First derivative for data list
 - Second derivative for data list
 + Findpeaks - Local maxima locator

Integration :
 - Simpsons adaptive trapezoidal method
 - Simpsons method for list data

ODE Integration :
 - Basic Euler method
 - Midpoint method
 - Adaptive RK 4/5 method
 - 4th order Runge-Kutta method
 - Richardson extrapolation-midpoint method

Curve Fitting :
 - Lin_reg : Linear regression least squares best fit line for data
 - Lin_origin : Least squares regression line through origin
 - Exp_reg

*** NEEDS WORK ***
LU decomposition worked with the homework set but did not pass when it got added to this module stack.
    - check differences between matlab code submission for homework and this module.
Matrix pivoting returns the augmented pivoted matrix, it would be handy if it broke the matrix back into a and b forms.
Verify that the differentiation formulas are working correctly, it generated an erroneous hit on the findpeaks function last time for heat/mass project first data point of 10 year temp data
Richardson extrapolation and midpoint method needs comments and testing
'''
import math as math # Built-in python module
import numpy as np # http://www.numpy.org Computing library with tools for scientific computing.

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
    return x_guess3, y_guess3

def newton_raphson(funct, fderiv, initial_guess, er_limit=0, max_iter=10):
    '''
    Numerical Methods - Roots of functions

    Newton-Raphson Method

    These open methods do not require both of the initial guesses to straddle
    the root, but sometimes these methods do not converge.
    Newton-Raphson is one of the more widely used algorithms.

    These methods converge at least twice as fast as bracketing methods


    funct : The function you are finding the root for
    fderiv : The first derivative of funct
    initial_guess : Starting point for calculation
    er_limit : Estimated Error Threshold (Optional)
    max_iter : Maximum iterations (Optonal, default is 10)

    '''
    x_guess = initial_guess
    for iter_no in range(max_iter):
        old_guess = x_guess
        y_guess = funct(x_guess)
        dy_guess = fderiv(x_guess)
        x_guess = x_guess - y_guess / dy_guess
        # Calculate the current estimated error on this iteration
        c_error = abs((x_guess - old_guess) / x_guess)
        if c_error < er_limit:
            # The calculated error has dropped below the required threshold
            break
    print('\nNewton-Raphson Method Results : \n')
    print('Approximated Value : {}'.format(x_guess))
    print('Function Output : {}'.format(y_guess))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    return x_guess, y_guess

def nm_secant(funct, xi_1 , xi, er_limit=0, max_iter=100):
    '''
    Numerical Methods - Roots of functions

    Secant Method

    These open methods do not require both of the initial guesses to straddle
    the root, but sometimes these methods do not converge.


    funct : The function you are finding the root for
    xi_1 : The i+1 term of the x starting values
    xi : The i-th term of starting values
    er_limit : Estimated Error Threshold (Optional)
    max_iter : Maximum iterations (Optional, default is 10)

    '''
    # Gather information on the function at the starting points
    x_plus1 = xi_1
    y_plus1 = funct(x_plus1)
    x_guess = xi
    y_guess = funct(x_guess)
    # Iterate within the loop parameters
    for iter_no in range(max_iter):
        # Store the previous values
        x_plus2 = x_plus1
        y_plus2 = y_plus1
        x_plus1 = x_guess
        y_plus1 = y_guess
        # Generate a new guess and output
        x_guess = x_plus1 - (y_plus1 * (x_plus2 - x_plus1))/(y_plus2 - y_plus1)
        y_guess = funct(x_guess)
        # Calculate the current estimated error on this iteration
        c_error = abs((x_guess - x_plus1) / x_guess)
        if c_error < er_limit:
            # The calculated error has dropped below the required threshold
            break
    print('\nSecant Method Results : \n')
    print('Approximated Value : {}'.format(x_guess))
    print('Function Output : {}'.format(y_guess))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    return x_guess, y_guess

def gauss_elim(input_coeff_mat,known_array):
    '''
    Numerical Methods : Gauss Elimination

    Solves a system of equations using matrix of coefficients and array of
    known_index values. This is a two step process:
    1. ) Forward elimination yields an upper triangular matrix
    2. ) Back substitution solves the equations and assembles the solution
            matrix

    input_coef_matrix : Array of coefficients for the equations we are trying to solve
    known_array : Array of constants
    '''
    # Get the dimensions of the coefficient matrix to make sure it is square
    m_rows = len(input_coeff_mat)
    n_cols = len(input_coeff_mat[0])
    if m_rows != n_cols:
        print('Input matrix must be square')
        exit
    # Generate an augmented combined matrix that includes the known value vector to make it easier to swap rows
    aug_comb = input_coeff_mat
    for row in aug_comb:
        new_col = known_array[aug_comb.index(row)]
        row.append(new_col)
    # Forward Elimination
    for pivot_row in range(n_cols):
        # Get the largest absolute value for the coefficients
        big = max(aug_comb[pivot_row][:-1], key=abs)
        # find the index of this value - Wonky way to handle this...
        big_index = [i for i, j in enumerate(aug_comb[pivot_row][:-1]) if j == big]
        # If the row largest value is not in the diagonal
        if big_index[0] != pivot_row:
            # Swap rows. Python is interpreted from left to right so this is cool
            aug_comb[pivot_row], aug_comb[big_index[0]] = aug_comb[big_index[0]], aug_comb[pivot_row]
        # Now that we have exhausted all options for getting the largest absolute
        # value onto the diagonal, we can move on.
        for elim_row in range(pivot_row + 1, n_cols):

            factor = aug_comb[elim_row][pivot_row]/aug_comb[pivot_row][pivot_row]
            # print('elim_row = {}  i = {}  factor = {}'.format(elim_row,pivot_row, factor))
            for item in range(n_cols + 1):
                aug_comb[elim_row][item] -= factor * aug_comb[pivot_row][item]
    # At this point, both the coefficient matrix and the elim_rownown value array have been transformed
    # into an upper triangular matrix that can be used to solve for the unknown values
    # BACK SUBSTITUTION - Solve the system of equations from bottom to top
    results = []
    # Use iterations of 'calc_row' to determine the distance from the bottom of the matrix to find
    # solutions for the values starting from the last row and ending once the first row has been calculated
    for calc_row in range(-1,-(m_rows+1),-1):
        # Initiate a value to hold the sum of the known variables and coefficients
        total = 0
        # Iterations of 'found_value' begin at -1 and stop when equal to the row we are calculating.
        # this loop is not entered for the first iteration because calc_row begins at -1
        for found_value in range(-1,calc_row,-1):
            # For each value that has been found so far, multiply the coefficient matrix
            # values for this row by the found values and sum them. The aug_comb offset is to compensate
            # for the addition of the known values at the beginning
            total += results[found_value]*aug_comb[calc_row][found_value-1]
        # Subtract the sum of the known quantities from the given input array for the row we are calculating
        # Divide all of this by the coefficient of the unknown variable to find the value for the unknown.
        # Do some fancy maneuvering to append this to the top of the output list, building the solution
        # from the bottom up. Once again, these results need to be offset by the extra column on the right.
        results = [(aug_comb[calc_row][-1] - total) / aug_comb[calc_row][calc_row-1]] + results
    # print('Results : {}'.format(results))
    return results

def gauss_seidel(coef_A,vec_B,guess_x=None, i_max=100, er_lim=.0001, rel_lam=1):
    '''
    Numerical Methods - Gauss-Seidel Method

    Most commonly used iterative method
    Fast convergence (when this works) helps to control round-off error
    Relaxation uses a value to attenuate the movement - speeds up convergence

    Problems:
        1.) Can be nonconvergent
        2.) Can converge slowly
    Benefits:
        1.) Less computationally heavy
        2.) Fastest method
        3.) Convergence guaranteed for diagonally dominant matrices

    coef_A : Input coefficient matrix
    vec_B : Known value vector
    guess_x : Initial guesses for x (optional, default is zeros)
    i_max : Maximum iterations (optional, default is 100)
    er_lim : Estimated error threshold (optional, default is 0.001)
    rel_lam : Initial relaxation coefficient lambda (optional, default is 1)

    Returns a list of values for the solution
    '''
    # Get the size of the input coefficient matrix and make sure it is square
    m_rows = len(coef_A)
    n_cols = len(coef_A[0])
    if m_rows != n_cols:
        print('Coefficient matrix must be square')
        exit
    # If no initial guess values are specified, instantiate a row of zeros for the solutions
    if guess_x == None:
        guess_x = [0 for i in range(m_rows)]
    # Here i addresses the container for each row in the matrix list
    for i in range(m_rows):
        # Store the original value of the diagonal value for this row of the input matrix
        dummy = coef_A[i][i]
        # j is addressing the individual item within the list for the coefficient row
        for j in range(m_rows):
            # Dividing the rest of the coefficients by the coefficient on the diagonal
            coef_A[i][j] = coef_A[i][j]/dummy
        # Since we did dummy division on the input matrix, we need to do it to the known vector
        vec_B[i] = vec_B[i]/dummy
    # Iterate across the rows again
    for i in range(m_rows):
        # Keep a total starting with the input matrix
        total = vec_B[i]
        # Move down the values in the row
        for j in range(m_rows):
            # On the values that are not on the diagonal
            if i != j:
                # Subtract the product of coefficient and guess
                total -= coef_A[i][j]*guess_x[j]
        # Store the total in this row of the output matrix
        guess_x[i] = total
    # Iterates until max iterations are met at most
    for _ in range(i_max):
        # Sentinel is a marker to flag when one of the error criteria are met
        sentinel = 1
        # Moves down the rows
        for i in range(m_rows):
            # Stores the previous value
            old = guess_x[i]
            # Initiates a running total starting with the first value from the input matrix
            total = vec_B[i]
            # j addresses the items in each row
            for j in range(m_rows):
                # When we are not computing a diagonal row
                if i != j:
                    # Subtract the off diagonal coefficients with their guess product
                    total -= coef_A[i][j] * guess_x[j]
            # Generate a new value for the guess matrix
            guess_x[i] = rel_lam * total + (1-rel_lam) * old
            # Enter this if statement when a value is stored in this value of the matrix
            if sentinel == 1 and guess_x[i] != 0:
                # Calculate current error for this iteration
                c_error = abs((guess_x[i] - old)/guess_x[i])*100
                # Set sentinel to zero if the current error is still outside the threshold
                if c_error > er_lim:
                    sentinel = 0
        # If the program has made it this far and sentinel is still 1, then an error
        # threshold has been met.
        if sentinel == 1:
            break
    return guess_x

def mat_inverse(input_matrix):
    '''
    Computes the inverse of a given matrix through LU Decomposition, forward, and back substitution
    '''
    # Get the size of the matrix and make sure it is square
    m_rows = len(input_matrix)
    n_cols = len(input_matrix[0])
    if m_rows != n_cols:
        print('Input matrix must be square')
        exit
    # Generate an identity matrix for the input matrix
    vec_B = [[float(i==j) for i in range(m_rows)] for j in range(m_rows)]
    # Decompose the input matrix into lower and upper triangular matrices
    lowr, upr = lu_decomp(input_matrix)
    # Instantiate a list for the output solutions
    solution = []
    # Run the LU Decomposition / back and forward substitution for each row in the identity matrix
    for row in vec_B:
        res_D = forward_sub(lowr, row)
        # Append each new value to the end of the solution list
        solution.append(back_sub(upr,res_D))
    return solution

def mat_mult(mat_m, mat_n):
    '''
    Multiplies two matrices m and n
    '''
    # Generate a matrix of zeros to hold the output
    result = [[0] * len(mat_m) for z_col in range(len(mat_n[0]))]
    # Iterate across rows
    for row in range(len(mat_m)):
        # Then go by column
        for col in range(len(mat_n[0])):
            # Then select each value from the matrices
            for val in range(len(mat_n)):
                # Change the value in the zero matrix
                result[row][col] += mat_m[row][val] * mat_n[val][col]
    return result

def mat_pivot(in_matrix):
    '''
    Pivots the input matrix to put the largest value on the diagonal. Returns an identity
    matrix that needs to be multiplied into the original matrix to yield the original
    transformed matrix
    '''
    n_row = len(in_matrix)
    # Generates an identity matrix using the result of the boolean test that runs down the
    # column and row for the matrix size.
    identity_mat = [[float(i==j) for i in range(n_row)] for j in range(n_row)]
    for item in range(n_row):
        # Rearrange the identity matrix so that the largest absolute value for each element
        # is on the diagonal
        row = max(range(item, n_row), key=lambda i: abs(in_matrix[i][item]))
        if item != row:
            # Swap the rows
            identity_mat[item], identity_mat[row] = identity_mat[row], identity_mat[item]
    return identity_mat

def lu_decomp(input_matrix, pivot=True):
    '''
    Yields the lower and upper decomposition for the input matrix (must be square)
    (optional) Cancel the pivoting step, default is to pivot.
    Returns :
    lower : Lower triangular matrix
    upper : Upper triangular matrix
    This method is slower than the numpy version but this is a breakdown of how it is done.
    '''
    # Get the size of the coefficient matrix and make sure it is square
    n_size = len(input_matrix)
    n_cols = len(input_matrix[0])
    if n_size != n_cols:
        print('Coefficient matrix must be square')
        exit
    # Generate zero matrices for lower and upper
    lower = [[0] * n_size for i in range(n_size)]
    upper = [[0] * n_size for i in range(n_size)]
    # Create pivot matrix pivot and multiplied matrix new_mat
    if pivot == True:
        pivot = mat_pivot(input_matrix)
        new_mat = mat_mult(pivot,input_matrix)
    else:
        new_mat = input_matrix
    # Perform LU Decomposition on each computation row
    # Here, each computation row will be calculated by iterating through each row of the matrix from top to bottom
    for comp_row in range(n_size):
        # All diagonal numbers for lower are set to 1
        lower[comp_row][comp_row] = 1
        # Here i is addressing the list elements that are contained within the row
        for i in range(comp_row+1):
            # Get the sum of the upper known value*coefficient pairs
            # k addresses each individual item in the new coefficient array
            sum_up = sum(upper[k][comp_row] * lower[i][k] for k in range(i))
            upper[i][comp_row] = new_mat[i][comp_row] - sum_up
        # This is essentially a matrix containing a list of the factor numbers from naive gauss.
        # i addresses the list
        for i in range(comp_row, n_size):
            # Computing the coefficients by taking the sum of the known value*coefficient pairs
            # Assign the lower matrix list item i for the computation row
            sum_low = sum(upper[k][comp_row]* lower[i][k] for k in range(comp_row))
            lower[i][comp_row] = (new_mat[i][comp_row] - sum_low) / upper[comp_row][comp_row]
    return lower, upper

def back_sub(input_matrix, known_values):
    '''
    Performs back substitution on a given input matrix with a vector of known values.
    Returns the results for the coefficients
    '''
    # Get the size of the coefficient matrix and make sure it is square
    a_rows = len(input_matrix)
    a_cols = len(input_matrix[0])
    if a_rows != a_cols:
        print('Input matrix must be square')
        exit
    results = []
    # Use iterations of 'calc_row' to determine the distance from the bottom of the matrix to find
    # solutions for the values starting from the last row and ending once the first row has been calculated
    for calc_row in range(-1,-(a_rows+1),-1):
        # Initiate a value to hold the sum of the known variables and coefficients
        total = 0
        # Iterations of 'found_value' begin at -1 and stop when equal to the row we are calculating.
        # this loop is not entered for the first iteration because calc_row begins at -1
        for found_value in range(-1,calc_row,-1):
            # For each value that has been found so far, multiply the coefficient matrix
            # values for this row by the found values and sum them.
            total += results[found_value]*input_matrix[calc_row][found_value]
        # Subtract the sum of the known quantities from the given input array for the row we are calculating
        # Divide all of this by the coefficient of the unknown variable to find the value for the unknown.
        # Do some fancy maneuvering to append this to the top of the output list, building the solution
        # from the bottom up.
        results = [(known_values[calc_row] - total) / input_matrix[calc_row][calc_row]] + results
    return results

def forward_sub(input_matrix, known_values):
    '''
    Performs forward substitution on a given input coefficient matrix and a vector matrix of known values.
    Returns a results vector matrix that can be sent into the back substitution method.
    '''
    # Get the size of the coefficient matrix and make sure it is square
    a_rows = len(input_matrix)
    a_cols = len(input_matrix[0])
    if a_rows != a_cols:
        print('Input matrix must be square')
        exit
    results = [known_values[0]]
    # Use iterations of 'calc_row' to determine the distance from the bottom of the matrix to find
    # solutions for the values starting from the last row and ending once the first row has been calculated
    for calc_row in range(1,a_rows):
        # Initiate a value to hold the sum of the known variables and coefficients
        total = 0
        # Iterations of 'found_value' begin at -1 and stop when equal to the row we are calculating.
        # this loop is not entered for the first iteration because calc_row begins at -1
        for found_value in range(calc_row):
            # For each value that has been found so far, multiply the coefficient matrix
            # values for this row by the found values and sum them.
            total += results[found_value]*input_matrix[calc_row][found_value]
        # Subtract the sum of the known quantities from the given input array for the row we are calculating
        # Divide all of this by the coefficient of the unknown variable to find the value for the unknown.
        # Do some fancy maneuvering to append this to the top of the output list, building the solution
        # from the bottom up.
        results += [(known_values[calc_row] - total) / input_matrix[calc_row][calc_row]]
    return results

def thomas(f_diag, e_diag, g_diag, b_vec):
    '''
    Numerical Methods : Thomas Algorithm

    A computationally lightweight method for solving tridiagonal matrices

    [ f(0) g(0)                           ][ x(0) ]   [ b(0) ]
    [ e(1) f(1) g(1)                      ][ x(1) ]   [ b(1) ]
    [      e(2) f(2) g(2)                 ][ x(2) ]   [ b(2) ]
    [            ...   ...   ...          ][ ...  ] = [ ...  ]
    [                e(n-1) f(n-1) g(n-1) ][x(n-1)]   [b(n-1)]
    [                        e(n)   f(n)  ][ x(n) ]   [ b(n) ]

    f_diag = Primary diagonal
    e_diag = Bottom coefficients - begins with a zero
    g_diag = Top coefficients - ends with a zero
    b_vec = Known vector quantities

    Returns a list of solved values
    '''
    # Get the number of values to find
    n = len(b_vec)
    # Append zero to beginning of e matrix
    e_diag = [0] + e_diag
    # Append zero to end of g matrix
    g_diag.append(0)
    # Initiate a solution vector full of zeros
    sol_vec = [0 for i in range(n)]
    # Decomposition
    for k in range(1,n):
        e_diag[k] /= f_diag[k-1]
        f_diag[k] -= e_diag[k] * g_diag[k-1]
    # Forward substitution
    for k in range(1,n):
        b_vec[k] -= e_diag[k] * b_vec[k-1]
    # Back substitution
    sol_vec[-1] = b_vec[-1]/f_diag[-1]
    for k in range(n-2,-1,-1):
        sol_vec[k] = (b_vec[k] - g_diag[k] * sol_vec[k+1]) / f_diag[k]
    return sol_vec


def golden(func, x_lower, x_upper, er_max=0.0001, it_max=100, maxima=True):
    '''
    One-Dimensional Unconstrained Optimization:
    Golden Section Search

    Finds the maximum or minimum for an input function between two given points
    using the golden ratio.

    func : Input function to evaluate
    x_low : Lower bound
    x_high : Upper bound
    er_max : Error threhsold (Optional, default is 0.0001)
    it_max : Max iterations (Optional, default is 100)
    maxima : When true, finds local maximum, when false, finds local minimum

    Returns x value, y value, error
    '''
    # Set up golden ratio as a constant
    R = (5**(0.5)-1)/2
    # Store the initial values in variables that will change within the function
    x_low = x_lower
    x_high = x_upper
    # Current error
    c_error = 1
    # Find movement through the first iteration
    d = R*(x_high - x_low)
    # Generate low and high guesses for the new x values
    x_one = x_low + d
    x_two = x_high - d
    # Find the function output from these two guesses
    y_one = func(x_one)
    y_two = func(x_two)
    # Iterate within the limits of the maximum number of iterations
    for iter_num in range(it_max):
        # Check for convergence
        if c_error < er_max:
            print('Met error threshold after {} iterations.'.format(iter_num))
            break
        # If we are finding the maximum, and y_one is greater, or vice versa
        if ((y_one > y_two) and (maxima == True)) or ((y_one < y_two) and (maxima == False)):
            # Store the low value in
            x_low = x_two
            x_two = x_one
            x_one = x_low + R * (x_high - x_low)
            y_one = func(x_one)
            y_two = func(x_two)
            c_error = (1 - R) * abs((x_high - x_low) / x_one)
        else:
            x_high = x_one
            x_one = x_two
            x_two = x_high - R * (x_high - x_low)
            y_one = func(x_one)
            y_two = func(x_two)
            c_error = (1 - R) * abs((x_high - x_low)/x_two)
        if ((y_one > y_two) and (maxima == True)) or ((y_one < y_two) and (maxima == False)):
            x_opt = x_one
        else:
            x_opt = x_two
    return x_opt, func(x_opt), c_error

def newton_optimize(funct, fderiv, f2deriv, initial_guess, er_limit=0, max_iter=10):
    '''
    Numerical Methods - Newton Raphson Optimization

    Newton-Raphson Method

    These open methods do not require both of the initial guesses to straddle
    the root, but sometimes these methods do not converge.
    Newton-Raphson is one of the more widely used algorithms.

    These methods converge at least twice as fast as bracketing methods


    funct : The function you are finding the root for
    fderiv : The first derivative of funct
    f2deriv : The second derivative of funct
    initial_guess : Starting point for calculation
    er_limit : Estimated Error Threshold (Optional)
    max_iter : Maximum iterations (Optonal, default is 10)

    '''
    x_guess = initial_guess
    for iter_no in range(max_iter):
        old_guess = x_guess
        y_guess = fderiv(x_guess)
        dy_guess = f2deriv(x_guess)
        x_guess = x_guess - y_guess / dy_guess
        # Calculate the current estimated error on this iteration
        c_error = abs((x_guess - old_guess) / x_guess)
        if c_error < er_limit:
            # The calculated error has dropped below the required threshold
            print('Error threshold met within {} iterations.'.format(iter_no))
            break
    print('\nNewton-Raphson Optimization Results : \n')
    print('Approximated Value : {}'.format(x_guess))
    print('Function Output : {}'.format(funct(x_guess)))
    print('Estimated Error : {}'.format(c_error))
    print('Iteration Count : {}'.format(iter_no + 1))
    return x_guess, funct(x_guess)

def cfdd_1deriv(fcn, val, step):
    '''
    Numerical Methods : Numeric Differentiation

    Centered Finite Divided Difference - 1st Derivative

    Calculates the derivative of a function numerically

    fcn : Function to evaluate
    val : Value to evaluate the function at
    step : Step size for generating the estimation

    Returns derivative
    '''
    # Get two steps away
    t_step = 2*step
    # Function minus 2 steps
    fx_m2 = fcn(val - t_step)
    # Function minus 1 step
    fx_m1 = fcn(val - step)
    # Function plus 1 step
    fx_p1 = fcn(val + step)
    # Function plus 2 steps
    fx_p2 = fcn(val + t_step)
    # Run through Taylor series approximation
    return ((-fx_p2 + 8*fx_p1 - 8*fx_m1 + fx_m2)/(12*step))

def num_1deriv(x_list, y_list):
    '''
    Numerical Methods - Numeric Differentiation of a list of data points
    returns first derivative
    centered finite difference with error = (O(h^2)) first two points and last two points are not valid.
    '''
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    # Check for dimension mismatch and data length
    if n_size != len(x_list):
        print('Numerical Differentiation Error (num_1deriv)\nSize of x-list and y-list must be the same\n')
        exit()
    # It needs at least 2 points to work
    elif n_size < 2:
        print('Numerical Differentiation Error (num_1deriv)\nData must be at least 2 values long.\n')
    # Preallocating the output list saves time in most languages, but doesn't really matter in python
    out_list = [None] * n_size
    # Runs through each case for the data points and returns the numerically derived derivative at the
    # given point for the whole list of data.
    for i_x in range(n_size):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_2 + 4*p_1 -3*y_list[i_x]) / (2*st_sz)
        elif i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x + 1]
            m_1 = y_list[i_x - 1]
            f_deriv = (p_1 - m_1) / (2 * st_sz)
        elif i_x == (n_size - 1):
            # Last data point uses Backward Finite Divided Difference
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (3*y_list[i_x] - 4*m_1 + m_2) / (2*st_sz)
        else:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 8*p_1 - 8*m_1 + m_2)/(12*st_sz)
        out_list[i_x] = f_deriv
    return out_list

def num_2deriv(x_list, y_list):
    '''
    Numerical Methods - Numeric Differentiation of a list of data points
    returns second derivative
    Forward Finite Divided difference at the start, Backward at the end, and centered in the middle
    Empirically, the error seems the worst at the second point and the second to last point with the
    more error prone centered divided difference formulas. potential future work may be to
    improve the error by using a more accurate forward or backward finite difference formula
    '''
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    if n_size != len(x_list):
        print('Numerical Differentiation Error (num_2deriv)\nSize of x-list and y-list must be the same\n')
        exit()
    elif n_size < 2:
        print('Numerical Differentiation Error (num_2deriv)\nData must be at least 2 values long.\n')
    # Preallocating the output list saves time in most languages, but doesn't really matter in python
    out_list = [None] * n_size
    # Runs through each case for the data points and returns the numerically derived derivative at the
    # given point for the whole list of data.
    for i_x in range(n_size):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_3 = y_list[i_x+3]
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_3 + 4*p_2 - 5*p_1 + 2*y_list[i_x])/(st_sz**2)
        elif i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            f_deriv = (p_1 - 2*y_list[i_x] + m_1)/(st_sz**2)
        elif i_x == n_size -1:
            # Last data point uses Backward Finite Divided Difference
            m_3 = y_list[i_x-3]
            m_2 = y_list[i_x-2]
            m_1 = y_list[i_x-1]
            f_deriv = (2*y_list[i_x] - 5*m_1 + 4*m_2 - m_3)/(st_sz**2)
        else:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 16*p_1 - 30*y_list[i_x] + 16*m_1 - m_2)/(12*st_sz**2)
        # Saves each point in its appropriate spot in the output list
        out_list[i_x] = f_deriv
    return out_list

def findpeaks(x_list, y_list):
    '''
    Accepts lists of x values and y-values from raw input data.
    Returns list of indices for detected peaks. Requires filtered data.
    '''
    dy_list = num_1deriv(x_list, y_list)
    d2y_list = num_2deriv(x_list, y_list)
    peak_points = []
    sign_toggle = 0
    n_pts = len(x_list)
    for x_i in range(n_pts):
        sign = sign_toggle
        if dy_list[x_i]*-1 > 0:
            # negative
            sign = 0
        else:
            sign = 1
        if sign != sign_toggle:
            sign_toggle = sign
            if d2y_list[x_i] < 0:
                peak_points.append(x_i)
    return peak_points

def sim_int(fcn, l_bnd, u_bnd, n_point):
    '''
    Numerical Methods - Closed Numerical Integration

    Simpson's Rules

    Numerically integrates a function within lower and upper bounds over
    a given number of data points using second and third order Lagrange
    polynomials to approximate the function

    fcn : Function to integrate
    l_bnd : Lower bound on integration
    u_bnd : Upper bound on integration
    n_point : Number of data points to consider

    returns sum of the area below the curve of the function
    '''
    # Trapezoidal area
    trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2
    def simp_38(h, f_0, f_1, f_2, f_3):
        '''
        Simpson's 3/8ths rule: Approximates a 3rd order Lagrange
        polynomial fit to four points.
        '''
        return (3*h * ((f_0 + 3 * (f_1 + f_2) + f_3) / 8))
    def simp_13m(fcn, h, n):
        '''
        Simpson's 1/3rd rule: Multiple Application: Feed a function,
        height and number of points. Needs odd number of points
        '''
        simp13_sum = fcn(0)
        for i in range(2, n-1, 2):
            simp13_sum += (4 * fcn((i-1)*h)) + (2 * fcn(h*(i-2)))
        simp13_sum += (4 * fcn(h*(n-2)) + fcn(h*(n-1)))
        return (h * simp13_sum / (3))
    # Step height across the function
    height = (u_bnd - l_bnd)/(n_point-1)
    # Instantiate a variable to hold sum of the total integral
    st_int = 0
    # Check for application of trapezoid method
    if n_point == 1:
        st_int = trap(height, fcn(0), fcn(1))
    elif n_point > 1:
        # Stores a mutable version to hold number of points
        m_point = n_point
        # Determine if the number of points is odd
        if (n_point % 2) == 0:
            f_0 = fcn(height*(n_point - 4))
            f_1 = fcn(height*(n_point - 3))
            f_2 = fcn(height*(n_point - 2))
            f_3 = fcn(height*(n_point - 1))
            # The number of points is even, so use 3/8ths rule on the last 4 points
            st_int += simp_38(height, f_0, f_1, f_2, f_3)
            # Update the number of points to use 1/3rd rule on
            m_point -= 3
        if m_point > 1:
            # feed the rest of the points to Simpson's third
            st_int += simp_13m(fcn, height, m_point)
    return st_int

def sim_int_num(x_list, y_list):
    '''
    Numerical Methods : Integration
    Numerically integrates an xy list using an optimized simpson algorithm
    '''
    # Trapezoidal rule for 2 points
    trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2
    # Simpsons 1/3 rule for 3 points
    simp_13 = lambda h, f_0, f_1, f_2 : 2*h*(f_0 + 4*f_1 + f_2)/6
    # Simpsons 3/8 rule for 4 points
    simp_38 = lambda h, f_0, f_1, f_2, f_3 : (3*h * (f_0 + 3* (f_1 + f_2) + f_3) / 8)
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    # Save the size of the dataset to handle even numbers
    m_size = n_size
    # Error checking on the data set for dimension mismatch
    if n_size != len(x_list):
        print('Numerical Integration Error (sim_int_num)\nSize of x-list and y-list must be the same\n')
        exit()
    # This function needs at least 2 points to run
    elif n_size < 2:
        print('Numerical Differentiation Error (sim_int_num)\nData must be at least 2 values long.\n')
    out_list = []
    # Trapezoidal rule gives the worst estimate of all of the methods in this function
    # but you gotta work with what you got.
    if n_size == 2:
        out_list.append(trap(st_sz, y_list[0], y_list[1]))
    # Simpson's 1/3 only works with odd numbers of data points. Using simpson's 3/8
    # on the last 4 points of the dataset and subtracting 3 points from the 1/3
    # iteration limit will handle this.
    elif (n_size % 2) == 0:
        f_0 = y_list[n_size-4]
        f_1 = y_list[n_size-3]
        f_2 = y_list[n_size-2]
        f_3 = y_list[n_size-1]
        out_list.append(simp_38(st_sz, f_0, f_1, f_2, f_3))
        m_size -= 3
    if m_size > 1:
        for i_x in range(0, m_size - 1, 2):
            f_0 = y_list[i_x]
            f_1 = y_list[i_x + 1]
            f_2 = y_list[i_x + 2]
            out_list.append(simp_13(st_sz, f_0, f_1, f_2))
    return sum(out_list)

def euler(func, x_0, x_f, y_0, n):
    '''
    Numerical Methods - Differential Equation Initial Value Problems

    ** Requires NUMPY import **
    import numpy as np

    Euler Method:

    Inputs:
    func : function with variables in the form of f(x,y)
    x_0, x_f : beginning and end points to evaluate the integral
    y_0 : Initial value for the dependent variable(s). Feed a 2-D numpy array to solve multiple equations.
    n : Number of intervals to use between x_0, x_f

    Outputs:
    x : List of independent variable values
    y : List of dependent variable values for each equation
    '''
    # Determine the step size
    d_x = (x_f - x_0) / (n)
    # Create a vector of x-values
    x = np.linspace(x_0, x_f, n+1)
    # Generate a vector to hold y-values
    y = np.zeros([n+1])
    # Set the first initial value
    y[0] = y_0
    # Iterate through the calculation
    for i in range(1,n+1):
        # The next point is found by evaluating the function at this point
        y[i] = d_x*(func(x[i-1],y[i-1])) + y[i-1]
    # Return x and y vectors
    return x, y

def midp_int(func, x_0, x_f, y_0, n):
    '''
    Numerical Methods - Differential Equation Initial Value Problems

    ** Requires NUMPY import **
    import numpy as np

    Midpoint Method:

    Inputs:
    func : function with variables in the form of f(x,y)
    x_0, x_f : beginning and end points to evaluate the integral
    y_0 : Initial value for the dependent variable(s). Feed a 2-D numpy array to solve multiple equations.
    n : Number of intervals to use between x_0, x_f

    Outputs:
    x : List of independent variable values
    y : List of dependent variable values for each equation
    '''
    # Determine the step size
    d_x = (x_f - x_0) / (n)
    # Create a vector of x-values
    X = np.linspace(x_0, x_f, n+1)
    # Generate a vector to hold y-values
    Y = np.zeros([n+1])
    # Set the first initial value
    Y[0] = y_0
    # Iterate through the calculation
    for i in range(1,n+1):
        k1 = func(X[i-1],Y[i-1])
        # The next point is found by evaluating the function at this point
        y_temp = Y[i-1] + d_x*(k1/2)
        k2 = func(X[i-1] + (d_x/2), y_temp)
        Y[i] = Y[i-1] + d_x*k2

    # Return x and y vectors
    return X, Y

def richard_mid(func, x_0, x_f, y_0, tol=1e-4):
    '''
    Numerical Methods : Differential Equations, Initial Value Problems
    Solves Ordinary Differential Equations using both midpoint and richardson extrapolation
    '''
    def rm_mdpt(func, x_n, x_f, y_n, n_step):
        h = (x_f - x_n) / n_step
        y_0 = y_n
        y_1 = y_0 + h*func(x_n, y_0)
        for _ in range(n_step - 1):
            x_n = x_n + h
            y_2 = y_0 + 2*h*func(x_n, y_1)
            y_0 = y_1
            y_1 = y_2
        return(0.5*(y_1 + y_0 + h*func(x_n,y_2)))
    def richardson(r,k):
        for j in range(k-1,0,-1):
            const = (k/(k-1))**(2*(k-j))
            r[j] = (const*r[j+1] - r[j])/(const - 1)
        return

    kMax = 51
    n = len(y_0)
    r = np.zeros((kMax, n))
    n_stp = 2
    r[1] = rm_mdpt(func, x_0, x_f, y_0, n_stp)
    r_old = r[1].copy()

    for k in range(2, kMax):
        n_stp = 2*k
        r[k] = rm_mdpt(func, x_0, x_f, y_0, n_stp)
        richardson(r, k)
        e = math.sqrt(np.sum((r[1] - r_old)**2)/n)
        if e < tol : return r[1]
        r_old = r[1].copy()
    print('midpoint method did not converge')


def ode45py(func, x, y, st_sz=1.0e-4, tol=1.0e-6, iter_lim=50000):
    '''
    Numerical Methods: Differential Equations, Initial Value Problems

    4th-order / 5th-order Runge-Kutta Method
    Includes adaptive step size adjustment
    Imitates MATLAB ode45 functionality and output
    '''
    # Dormand-Prince coefficients for RK algorithm -
    a1 = 0.2; a2 = 0.3; a3 = 0.8; a4 = 8/9; a5 = 1.0; a6 = 1.0
    c0 = 35/384; c2 = 500/1113; c3 = 125/192; c4 = -2187/6784; c5=11/84
    d0 = 5179/57600; d2 = 7571/16695; d3 = 393/640; d4 = -92097/339200; d5 = 187/2100; d6 = 1/40
    b10 = 0.2
    b20 = 0.075; b21 = 0.225
    b30 = 44/45; b31 = -56/15; b32 = 32/9
    b40 = 19372/6561; b41 = -25360/2187; b42 = 64448/6561; b43 = -212/729
    b50 = 9017/3168; b51 = -355/33; b52 = 46732/5247; b53 = 49/176; b54 = -5103/18656
    b60 = 35/384; b62 = 500/1113; b63 = 125/192; b64 = -2187/6784; b65 = 11/84
    # Store initial values
    x_f = x[-1]
    x_n = x[0]
    # y_n = y
    # Initialize variables
    X = []
    Y = []
    # Add the first set of known conditions
    X.append(x_n)
    Y.append(y)
    # I need an iteration counter that has a scope outside the computation loop
    i_count = 0
    # Set up to break the for loop at the end
    stopper = 0 # Integration stopper, 0 = off, 1 = on
    # Initialize a k0 to start with the step size
    k0 = st_sz * func(x_n, y)
    # Generate the RK coefficients
    for i in range(iter_lim):
        # Store the iteration number in the other variable for feedback string
        i_count = i
        # Compute the 4th order / 5th order algorithm
        k1 = st_sz * func(x_n + a1*st_sz, y + b10*k0)
        k2 = st_sz * func(x_n + a2*st_sz, y + b20*k0 + b21*k1)
        k3 = st_sz * func(x_n + a3*st_sz, y + b30*k0 + b31*k1 + b32*k2)
        k4 = st_sz * func(x_n + a4*st_sz, y + b40*k0 + b41*k1 + b42*k2 + b43*k3)
        k5 = st_sz * func(x_n + a5*st_sz, y + b50*k0 + b51*k1 + b52*k2 + b53*k3 + b54*k4)
        k6 = st_sz * func(x_n + a6*st_sz, y + b60*k0 + b62*k2 + b63*k3 + b64*k4 + b65*k5)
        # Getting to the slope is the whole point of this mess
        dy = c0*k0 + c2*k2 + c3*k3 + c4*k4 + c5*k5
        # Determine the estimated change in slope by comparing the output coefficients for each RK coefficient
        E = (c0 - d0)*k0 + (c2 - d2)*k2 + (c3 - d3)*k3 + (c4 - d4)*k4 + (c5 - d5)*k5 - d6*k6
        # Find the estimated error using a sum of squares method
        e = math.sqrt(np.sum(E**2)/len(y))
        # Compute a new step size to go into the weighting algorithm
        hNext = 0.9*st_sz*(tol/e)**0.2

        # If approximated error is within tolerance, accept this integration step and move on
        if e <= tol:
            # Store the new result
            i = i-1
            y = y + dy
            # Increment the x-value by the new step size
            x_n = x_n + st_sz
            # Add the new values into the output vector
            X.append(x_n)
            Y.append(y)
            # Check to break the loop when we have reached the desired x-value
            if stopper == 1: break # Reached end of x-range
            # Set limits on how much the next step size can increase to avoid missing data points
            if abs(hNext) > 10*abs(st_sz): hNext = 10*st_sz
            # Determine if the algorithm has reached the end of the dataset
            if (st_sz > 0.0) == ((x_n + hNext) >= x_f):
                hNext = x_f - x_n
                # Sets the break condition for the next loop iteration
                stopper = 1


            # Setting k0 to k6 * (next step size) / (current step size) forces the algorithm to use the 4th order formula for the next step
            k0 = k6*hNext/st_sz
        else:
            # The error estimate is outside the required threshold to move on, we need to redo the calculation with a smaller step size
            if abs(hNext) < abs(st_sz)*0.1 : hNext = st_sz*0.1
            # Set up k0 to go through the 5th order RK method on the next iteration because the error was no good.
            k0 = k0*hNext/st_sz
        # Set the next iteration step size
        st_sz = hNext
    pcnt = (i_count/iter_lim)*100
    psolv = (x_n/x_f)*100
    print('ode45py _ Computation limit used : {:1.2f}%\n\tX-Domain Integrated: {:1.2f}%'.format(pcnt, psolv))
    # Returns the arrays for x and y values
    return np.array(X), np.array(Y)

def runge_kutta4(func, x_0, x_f, y_0, n=0, st_sz=0):
    '''
    Numerical Methods: Differential Equations, Initial Value Problems

    4th-order Runge-Kutta Method
    Does not include adaptive step size adjustment

    ** Requires numpy to return the np.array datatype and to handle the input vector in both func and y_0 **

    Input:
    func : Function to evaluate in the form F(x,y)
    x_0 : Initial value for x to start evaluating the integral
    x_f : Final value for x
    y_0 : Initial value for y when x = x_0
    n : Number of slices to use on the domain for the evaluation

    Output
    x : x-vector
    y : y-vector
    '''
    # Workhorse of the method - generates a weighted average for the slope estimate between the two points being evaluated
    def rk4(func, x_i, y_i, st_sz):
        k0 = st_sz*func(x_i, y_i)
        k1 = st_sz*func(x_i + st_sz/2.0, y_i + k0/2.0)
        k2 = st_sz*func(x_i + st_sz/2.0, y_i + k1/2.0)
        k3 = st_sz*func(x_i + st_sz, y_i + k2)
        return (k0 + 2.0*k1 + 2.0*k2 + k3)/6.0
    # Check for input on step size or number of segments
    if st_sz == 0 and n == 0:
        print('Error in Numeric Integration using RK4 method: Last argument must be either a step size or number of segments.\nUsage: X, Y = runge_kutta4(func, x_0, x_f, y_0, n=< # steps > ~OR~ st_sz=< step size >')
    # Generate a step size if number of segments is provided
    elif st_sz == 0:
        st_sz = (x_f - x_0) / n
    # Set up the initial values
    x_n = x_0
    y_n = y_0
    # Instantiate variables to hold the solutions
    X = []
    Y = []
    # Begin adding the intiial values to the solution vectors
    X.append(x_n)
    Y.append(y_n)
    # Generate the soltuion vector for the rest of the points
    while x_n < x_f:
        # Doing this handles the situation where not a big enough step size is provided
        st_sz = min(st_sz, x_f - x_n)
        y_n = y_n + rk4(func, x_n, y_n, st_sz)
        x_n = x_n + st_sz
        X.append(x_n)
        Y.append(y_n)
    # Set the solution in an array for easier numpy dumpy
    return np.array(X), np.array(Y)



def lin_reg(x_list, y_list):
    '''
    Generates linear regression best fit line for list of x-values and y-values passed in the form of a list
    Returns coefficients for the form y = a * x + b
    a, b, r_squared, std_er, er_max = lin_fit(x_list, y_list)
    a : a-coefficient
    b : intercept offset
    r_squared : correlation coefficient
    std_er : standard error
    er_max : maximum error
    '''
    # Gather information about the data set
    n = len(x_list)
    if n != len(y_list):
        print('Lists must be of equal length.')
        return
    s_xi = sum(x_list)
    s_yi = sum(y_list)
    y_mean = s_yi/n
    s_xi2 = sum([i**2 for i in x_list])
    s_xy = sum([x_list[i]*y_list[i] for i in range(n)])
    # Calculate coefficients
    coef_a = ((n * s_xy) - (s_xi * s_yi)) / ((n * s_xi2) - (s_xi**2))
    coef_b = ((s_xi2 * s_yi) - (s_xi * s_xy)) / ((n*s_xi2) - (s_xi**2))
    # Sum of the squares of residuals from the generated line
    s_sq_t = sum([((coef_a * x_list[i] + coef_b - y_list[i])**2) for i in range(n)])
    # Sum of the squares of residuals from the mean
    s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n)])
    # Standard deviation
    st_dev = (s_sq_r / (n-1))**(0.5)
    # R-Squared Value - coefficient of determination
    r_sq = 1 - (s_sq_t / s_sq_r)
    # Standard error
    std_er = (s_sq_t/(n-2))**(0.5)
    # Find maximum error deviation from the best fit line
    er_max = max([abs(coef_a * x_list[i] + coef_b - y_list[i]) for i in range(n)])
    print('Linear Best Fit: y = ( {:.4f} ) x {:+.4f}'.format(coef_a,coef_b))
    print('Standard Deviation = {:.4f}'.format(st_dev))
    print('R-Squared, Calibration Constant = {:.4f}'.format(r_sq))
    print('Standard Error = {:.4f}'.format(std_er))
    print('Maximum Error = {:.4f}\n'.format(er_max))
    return coef_a, coef_b

def lin_origin(x_list, y_list):
    '''
    Fits a line through the origin of the form y = a*x + 0 for instrument calibration
    applications.
    '''
    n_size = len(y_list)
    y_mean = sum(y_list)/n_size
    numer = 0
    denom = 0
    if n_size != len(x_list):
        print('Numerical Differentiation Error (lin_origin)\nSize of x-list and y-list must be the same\n')
        exit()
    for x_i in range(n_size):
        numer += x_list[x_i]*y_list[x_i]
        denom += x_list[x_i]**2
    coef_a = (numer/denom)
    s_sq_t = sum([((coef_a * x_list[i] - y_list[i])**2) for i in range(n_size)])
    s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n_size)])
    r_sq = 1 - (s_sq_t / s_sq_r)

    return coef_a, r_sq

def xexp_reg(x_data, y_data):
    '''
    Numerical Methods : Exponential curve fit
    Input x and y data points,

    Returns exponential curve fit constants A and b
    y = Ax * exp(b*x)
    '''
    # Get the size of the dataset
    size = len(x_data)
    # To get the desired regression equation result, we take the natural log of y_i/x_i
    ln_y = [math.log(y_data[i]/x_data[i]) for i in range(size)]

    # X_hat and Z_hat comes from using weighted averages for the data to generate a better fit
    x_hat_num = sum([(y_data[i]**2)*x_data[i] for i in range(size)])
    z_hat_num = sum([(y_data[i]**2)*ln_y[i] for i in range(size)])
    # Sum of y_data square
    sy_sq = sum([y_data[i]**2 for i in range(size)])
    # New coefficients for linear fit
    x_hat = x_hat_num / sy_sq
    z_hat = z_hat_num / sy_sq
    # Generate the b-parameter
    coef_b_num = sum([(y_data[i]**2) * ln_y[i] * (x_data[i] - x_hat) for i in range(size)])
    coef_b_den = sum([(y_data[i]**2) * x_data[i] * (x_data[i] - x_hat) for i in range(size)])
    coef_b = coef_b_num / coef_b_den
    # Find the A coefficient
    coef_A = np.exp(z_hat - coef_b * x_hat)
    # Set up the function to calculate residuals and give feedback on how the curve fits the data
    func = lambda x : x * coef_A * np.exp(coef_b * x)
    # Sum of the residuals from the calculation
    s_resi = sum([(y_data[i] - func(x_data[i]))**2 for i in range(size)])
    # Standard deviaton from the data. Small numbers are good here
    std_dev = (s_resi / (size - 2))**(0.5)
    # print('Exponential Curve Fit Standard Deviation : {}'.format(std_dev))
    return coef_A, coef_b, std_dev