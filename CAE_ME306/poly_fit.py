from NumericalMethods import gauss_elim
import numpy as np
import matplotlib.pyplot as plt

def poly_fit(x_data, y_data, deg):
    '''
    Numerical Methods : Curve Fitting data

    Polynomial regression

    Returns least squares polynomial of degree 'deg' fit to the set of data points
    '''
    a = np.zeros((deg+1, deg+1))
    b = np.zeros(deg+1)
    s = np.zeros(2*m+1)
    for i in range(len(x_data)):
        temp = y_data[i]
        for j in range(m+1):
            b[j] = b[j] + temp
            temp = temp*x_data[i]
        for i in range(m+1):
            for j in range(m+1):
                a[i,j] = s[i+j]
    return gauss_elim(a,b)

# def swap_rows(mat, row_a, row_b):
#     ''' Swaps row_a and row_b of matrix 'mat' '''
#     if len(mat.shape) == 1:
#         mat[row_a], mat[row_b] = mat[row_b], mat[row_a]
#     else:
#         mat[[row_a, row_b],:] = mat[[row_b, row_a],:]

# def swap_cols(mat, col_a, col_b):
#     ''' Swaps col_a and col_b of matrix 'mat' '''
#     mat[:,[col_a, col_b]] = mat[:,[col_b, col_a]]

# def gauss_pivot(mat_a , k_vec, tol=1.0e-12):
#     '''
#     Alternative gauss elimi
#     nsize = len(k_vec)
#     s

def plotPoly(xData,yData,coeff,xlab=’x’,ylab=’y’):
    m = len(coeff)
    x1 = min(xData)
    x2 = max(xData)
    dx = (x2 - x1)/20.0
    x = np.arange(x1,x2 + dx/10.0,dx)
    y = np.zeros((len(x)))*1.0
    for i in range(m):
        y = y + coeff[i]*x**i
    plt.plot(xData,yData,’o’,x,y,’-’)
    plt.xlabel(xlab); plt.ylabel(ylab)
    plt.grid (True)
    plt.show()

