## module prob6_9bc
'''
Test case for newton raphson and secant methods for finding roots of a function
'''
from newton_rhapson_and_secant import newton_raphson, nm_secant
def main():
    '''
    Associated with Problem 6.9 b & c
    '''

    # Initial functions to find the root
    funct = lambda x : x**3 - 6*x**2 + 11*x - 6.1
    # Derivative of the first function for Newton-Rhapson
    funct_p = lambda x : 3*x**2 - 12*x + 11
    x_init = 3.5 # Initial guess
    x_i = 2.5 # Initial first guess for the i term in secant method
    er_lim = 0.005 # Error limit of less than 0.5%
    max_i = 3 # Max iterations
    newton_raphson(funct, funct_p, x_init, er_lim, max_i)
    nm_secant(funct, x_init, x_i, er_lim, max_i)

main()