from numpy import exp
import numpy as np
import matplotlib.pyplot as plt
from NumericalMethods import ode45py, thomas
import math as math

def me306_final_1():
    # d2T/dx2 - 0.15T = 0
    side1 = 240 # Temperature of left side of rod (known)
    side2 = 150 # Temperature of right side of rod (known)
    iguess1 = -85# Initial guess for the rate of cooling along the rod
    iguess2 = -95 # Second guess for the rate fo cooling along the rod

    # Generate the analytical solution
    '''
    Ordinarily, I would put this simple 2 equation 2 unknown problem into a solver, but since I had to do it out by hand,
    I will just generate the numbers from the operations
    '''
    epow = 10 * (0.15)**(0.5)
    lside = side2 - side1*exp(epow)
    c_2 = lside / (exp(-epow) - exp(epow))
    c_1 = side1 - c_2
    # anonymous function to generate output points for the bar
    anal = lambda in_val : (c_1 * exp(in_val*(0.15**0.5)) + c_2 * exp(-in_val*(0.15**0.5)))
    dif_er = lambda x, y : abs((y-anal(x))/anal(x))*100
    # Set up the state function for the ODE solver
    def func(x, T):
        parray = np.zeros(2)
        parray[0] = T[1]
        parray[1] = 0.15*T[0]
        return parray
    # Generate analytical solution points
    X1 = np.arange(0, 11)
    Y1 = np.array([anal(i) for i in range(len(X1))])
    # Set up integration x segments
    x_startstop = [0,10]
    # The value we are shooting for
    needed_val = side2
    # Generate initial conditions for each of the guesses
    guess1 = np.array([side1, iguess1])
    guess2 = np.array([side1, iguess2])
    # set an initial step size. ode45py will adjust this, if we need to use constant step size, we could use runge_kutta4 in the NumericalMethods module
    h = 1
    # Call the ode solver for each initial condition
    Xa, Ya = ode45py(func, x_startstop, guess1, st_sz=h)
    Xb, Yb = ode45py(func, x_startstop, guess2 , st_sz=h)
    # Store the output values from each integration estimate
    output1 = Ya[:,0][-1]
    output2 = Yb[:,0][-1]
    print('Output 1 : {:1.2f}, Output 2 : {:1.2f}'.format(output1, output2))

    # check to make sure that the output values will work for an interpolation on our desired output codition
    if needed_val < output1:
        if output2 < needed_val:
            bound = True
    else:
        if output2 > needed_val:
            bound = True
        else:
            print('Initial guess end results fall on same side of known value of {} C. Select different guesses for initial temp rates.'.format(needed_val))
            return
    if bound:
        # Find the shooting method results
        lininterp = lambda p_in, p1, p2, q1, q2: (q1 * (p2 - p_in) + q2 * (p_in - p1)) / (p2 - p1)
        # Find shooting method interpolation as input for next ode integration
        shoot_dx0 = [240,lininterp(needed_val, output1, output2, guess1[-1], guess2[-1])]
        # Call the ode solver one more time to generate a solution
        X2, Y2 = ode45py(func, x_startstop, shoot_dx0 , st_sz=h)
        shoot_res = Y2[:,0][-1]
        sh_error = [dif_er(X2[i], Y2[i,0]) for i in range(len(X2))]
        # plt.plot(Xa, Ya[:,0], ':', label=r'Guess 1, $\frac{dT}{dx}$ = ' + '{}'.format(guess1[-1]) + r'$\frac{C}{m}$',c='C2')
        # plt.plot(Xb, Yb[:,0], ':', label=r'Guess 2, $\frac{dT}{dx}$ = ' + '{}'.format(guess2[-1]) + r'$\frac{C}{m}$',c='C3')
        # plt.plot(X2, Y2[:,0], 'o-', label=r'Shooting Result, $\frac{dT}{dx}$ = ' + '{:1.2f} , Error = {:.9f}'.format(shoot_dx0[-1], sum(sh_error)),c='C1')

    '''
    Using the centered finite difference formula for numeric differentiation, we can represent the rod as a 9 x 9 tridiagonal system
    This can be soved using the thomas algorithm
    '''
    # Matrix length
    mat_size = 9
    # Primary diagonal value
    prim_diag = 2.15
    # Top and bottom vectors
    top_bot = 1
    # The primary diagonal
    in_f = [prim_diag] * mat_size
    # Bottom coefficients
    in_e = [top_bot] * (mat_size-1)
    # Top coefficients
    in_g = in_e
    # known vector
    in_b = np.zeros(mat_size)
    # Set the boundary conditions
    in_b[0] = side1
    in_b[-1] = side2
    # Finite difference results using thomas algorithm)
    fin_dif = thomas(in_f, in_e, in_g, in_b)
    # Generate x-points for plotting and error calculations
    fin_x = range(1, len(fin_dif)+1)
    # The algorithm produced positive and negative values
    fin_y = [abs(i) for i in fin_dif]
    # Calculate the error from the analytical solution at each output point
    er_fin = [dif_er(fin_x[i], fin_y[i]) for i in range(len(fin_x))]
    # Create a list of the accumulated error as the calculation progresses
    accumulate = lambda in_list : [in_list[i] + sum(in_list[0:i]) for i in range(len(in_list))]
    # Store these lists for error analysis
    acc_sh_er = accumulate(sh_error)
    acc_fi_er = accumulate(er_fin)
    # plt.plot(fin_x, fin_y,'o', label='Finite Difference Solution, Error = {:.9f}'.format(sum(er_fin)), c='r')
    # plt.plot(X1, Y1, '-', label='Analytical Solution', c='k')
    # plt.xlabel('X - Values')
    # plt.ylabel('Y - Values')
    # plt.title('Boundary Problem Solution Methods')
    # plt.legend()
    # plt.savefig('ME399_prob_1b.png',bbox_inches='tight')
    # plt.show()

    plt.plot(X2, acc_sh_er,'o-', label='Shooting Method')
    # plt.plot(fin_x, acc_fi_er,'o-', label='Finite Difference Method')
    plt.xlabel('Distance from initial position (m)')
    plt.ylabel('Accumulated Percent Error')
    plt.title('Boundary Problem Accumulated Error')
    plt.legend()
    plt.savefig('ME399_prob_1cb.png',bbox_inches='tight')
    plt.show()

me306_final_1()
