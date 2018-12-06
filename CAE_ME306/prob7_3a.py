## module prob7_3a
'''
Test case for muller method for finding roots of functions'''
from muller_method import muller_method

def prob7_3a():
    f_x = lambda x : x**3 + x**2 - 4*x -4 # Function to evaluate
    x_0 = -3 # Guess 1
    x_1 = -2.5 # Guess 2
    x_2 = -1.5 # Guess 3
    muller_method(f_x, x_0, x_1, x_2)
prob7_3a()