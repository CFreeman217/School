## module prob5_16b
from bisection import bisection
def main():
    '''
    Problem 5-16b : Critical Depth of Trapezoidal Channel

    Bisection Method Results :

    Approximated Value : 1.5078125
    Function Output : -0.013595193182066145
    Estimated Error : 0.0051813471502590676
    Iteration Count : 8
    '''
    Q = 20 # m^3/s - Flow Rate
    g = 9.81 # m/s^2 - Gravity
    # Function to iterate over
    f = lambda y : 1 - (Q**2 / (g * (3*y + y**2/2)**3))*(3 + y)
    low = 0.5 # Lower Guess
    high = 2.5 # Upper Guess
    er = 0.01 # Boundary Limit
    m_it = 10 # Maximum Iterations
    # Call the bisection subroutine
    bisection(f, low, high, er, m_it)

main()
