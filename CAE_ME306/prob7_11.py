## module prob7_11
'''
Test case for muller method for finding roots of functions'''
from muller_method import muller_method
def prob7_11():
    from math import e
    g = 9.81 # m/s^2 Gravity
    c = 15 # kg/s Drag Coefficient
    v = 35 # m/s Velocity
    t = 8 # s Time
    f_x = lambda m : (g*m/c)*(1-e**(-c*t/m))-v # Function to evaluate
    x_0 = 1 # Guess 1
    x_1 = 50 # Guess 2
    x_2 = 100 # Guess 3
    muller_method(f_x, x_0, x_1, x_2)
prob7_11()