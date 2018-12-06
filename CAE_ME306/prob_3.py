## module prob_3
'''
Test case for Lin Reg using list of data points
See also: example17_1.py
'''
from lin_reg import lin_reg
def prob_3():
    deflect = [0.00, 1.25, 2.50, 3.75, 5.00]
    v_out = [0.10, 0.65, 1.32, 1.95, 2.70]
    m, b = lin_reg(deflect, v_out)


prob_3()