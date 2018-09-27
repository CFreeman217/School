import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

def mass_spring(mass, damp_coef, sp_const, i_disp):
    '''
    Damped spring mass response
    '''
    def dU_dx(U, x):
        grav = 9.81
        dU = U[1]
        d2U = (1/mass) * (mass*grav - (damp_coef*dU) - sp_const * U[0])
        return [dU, d2U]
    i_cond = [i_disp, 0]
    x_vals = np.linspace(0, 5, 1000)
    u_vals = integrate.odeint(dU_dx, i_cond, x_vals)
    y_vals = u_vals[:,0]
    plt.plot(x_vals, y_vals)
    plt.show()


mass_spring(4, 20, 2000, 60)
