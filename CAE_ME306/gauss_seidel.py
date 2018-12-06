## module gauss-seidel
'''
gauss_seidel(coef_A,vec_B,guess_x=None, i_max=100, er_lim=.0001, rel_lam=1)
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

See example11_3.py
'''

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


