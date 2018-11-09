## module gauss_elimination
'''
Numerical Methods - linear systems of equations

Gauss Elimination
    Solves a system of equations using matrix of coefficients and array of
    known_index values. This is a two step process:
    1. ) Forward elimination yields an upper triangular matrix
    2. ) Back substitution solves the equations and assembles the solution
            matrix

    input_coef_matrix : Array of coefficients for the equations we are trying to solve
    known_array : Array of constants
'''
def naive_gauss_pivot(input_coeff_mat,known_array):
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
    # At this point, both the coefficient matrix and the known value array have been transformed
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
    print('Results : {}'.format(results))
    return results


