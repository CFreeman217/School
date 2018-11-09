## module example17_1
'''
Test case for Lin Reg using list of data points
See also: prob_3.py
'''
from lin_reg import lin_reg
def ex17_1():
    y_i = [0.5,\
           2.5,\
           2.0,\
           4.0,\
           3.5,\
           6.0,\
           5.5]
    m, b = lin_reg([i for i in range(1,(len(y_i)+1))], y_i)


ex17_1()