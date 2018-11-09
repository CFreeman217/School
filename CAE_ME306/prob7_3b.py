## module prob7_3b
'''
Test case for muller method for finding roots of functions'''
from muller_method import muller_method
def prob7_3b():
    f_x = lambda x : x**3 - 0.5*x**2 + 4*x - 2 # Function to evaluate
    x_0 = -1 # Guess 1
    x_1 = 1 # Guess 2
    x_2 = 2 # Guess 3
    muller_method(f_x, x_0, x_1, x_2)
prob7_3b()