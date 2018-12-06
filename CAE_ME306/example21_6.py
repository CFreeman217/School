## module example21_6
'''
Test case for Simpson's Rules for numeric integration of both known functions and raw data output.
'''
import numpy as np
from sim_int import sim_int, sim_int_num
def ex21_6():
    func = lambda x : 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5
    low = 0
    high = 0.8
    n_seg = 6
    x_vals = np.linspace(low, high, n_seg)
    y_vals = np.array(func(x_vals))
    snum = sim_int_num(x_vals, y_vals)
    print(snum)
    print(sim_int(func, low, high, n_seg))
ex21_6()