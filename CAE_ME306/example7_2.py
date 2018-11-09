## module example7_2
'''
Test case for muller method for finding roots of functions'''
from muller_method import muller_method
def example7_2():
    f_x = lambda x : x**3 - 13*x -12 # Function to evlauate
    x_0 = 4.5 # Guess 1
    x_1 = 5.5 # Guess 2
    x_2 = 5 # Guess3
    muller_method(f_x, x_0, x_1, x_2)
example7_2()