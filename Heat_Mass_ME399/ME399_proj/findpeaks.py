## module findpeaks
'''Accepts list of x_values and y_values, performs numeric differentiation for first and second derivative. Returns peak values'''
from div_dif_deriv import num_1deriv, num_2deriv

def findpeaks(x_list, y_list):
    '''
    Accepts lists of x values and y-values from raw input data.
    Returns list of indices for detected peaks. Requires filtered data.
    '''
    dy_list = num_1deriv(x_list, y_list)
    d2y_list = num_2deriv(x_list, y_list)
    peak_points = []
    sign_toggle = 0
    n_pts = len(x_list)
    for x_i in range(n_pts):
        sign = sign_toggle
        if dy_list[x_i]*-1 > 0:
            # negative
            sign = 0
        else:
            sign = 1
        if sign != sign_toggle:
            sign_toggle = sign
            if d2y_list[x_i] < 0:
                peak_points.append(x_i)
    return peak_points