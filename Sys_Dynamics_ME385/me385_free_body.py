import math

def lifting_tongs():
    '''
    Solve the system of equations using LU Decomposition and back substitution
    '''
    len_a = 5 * (2.54/100)
    len_b = len_a # Between 5 and 9
    l_1 = 3 * (2.54/100)
    l_2 = l_1 # less than 4
    wgt = 100*4.44822
    alpha = 30 * (math.pi/180)
    r_vert = wgt/2
    r_horz = wgt/2 * (((len_a + len_b)/l_2) + (l_1/l_2) * math.cos(alpha))
    print(r_horz)
    # mat_A = [[ 3, -2, 1],
    #          [ 2,  6,-4],
    #          [-1, -2, 5]]
    # vec_B = [-10,
    #           44,
    #          -26]
    # lowr, upr = lu_decomp(mat_A)
    # print('Lower Matrix : ')
    # for line in lowr:
    #     print(line)
    # print('Upper Matrix : ')
    # for line in upr:
    #     print(line)
    # res_D = forward_sub(lowr,vec_B)
    # print('Forward Vector : ')
    # for line in res_D:
    #     print(line)
    # sol = back_sub(upr,res_D)
    # print('Solution : ')
    # for line in sol:
    #     print(line)

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

lifting_tongs()