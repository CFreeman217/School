from NumericalMethods import xexp_reg
import numpy as np
import matplotlib.pyplot as plt
import math as math

def final_2():
    # data set is given
    x_data = [0.5*(i+1) for i in range(5)]
    y_data = [0.541, 0.398, 0.232, 0.106, 0.052]
    # Run exp_reg and produce the requested data
    a_con, b_con , sd = xexp_reg(x_data, y_data)
    # Generate a list of points from the regression function
    y_reg = [i*a_con*np.exp(b_con*i) for i in x_data]
    # Create the plot
    plt.plot(x_data, y_data,'o')
    plt.plot(x_data, y_reg)
    plt.text(.5, .1, r'Std. Deviation, $\sigma$ = {:1.6f}'.format(sd))
    plt.xlabel('X - Values')
    plt.ylabel('Y - Values')
    plt.title('Log fit for data : y = {:1.2f}x * '.format(a_con) + r'e$^{' + '{:1.2f}x'.format(b_con) + r'}$')
    plt.savefig('ME306_final_prob2.png', bbox_inches='tight')
    plt.show()

final_2()