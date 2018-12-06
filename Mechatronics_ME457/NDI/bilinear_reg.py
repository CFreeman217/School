'''Linear Regression using 2 variables'''

y_data = [1,
          2,
          1,
          3,
          2,
          3,
          3,
          4,
          4,
          3,
          5,
          3,
          3,
          2,
          4,
          5,
          5,
          5,
          4,
          3]
x1_data = [40,
           45,
           38,
           50,
           48,
           55,
           53,
           55,
           58,
           40,
           55,
           48,
           45,
           55,
           60,
           60,
           60,
           65,
           50,
           58]
x2_data = [25,
           20,
           30,
           30,
           28,
           30,
           34,
           36,
           32,
           34,
           38,
           28,
           30,
           36,
           34,
           38,
           42,
           38,
           34,
           38]

def bilin_reg(x_list, y_list, z_list):
    n_pts = len(x_list)
    xy = [x_list[i] * y_list[i] for i in range(n_pts)]
    xz = [x_list[i] * z_list[i] for i in range(n_pts)]
    yz = [y_list[i] * z_list[i] for i in range(n_pts)]
    s_xi = sum(x_list)
    s_yi = sum(y_list)
    s_zi = sum(z_list)
    x_mean = s_xi/n_pts
    y_mean = s_yi/n_pts
    z_mean = s_zi/n_pts
    s_xy = sum(xy)-(s_yi*s_xi)/n_pts
    s_xz = sum(xz)-(s_zi*s_xi)/n_pts
    s_yz = sum(yz)-(s_yi*s_zi)/n_pts
    s_x_2 = sum([(x_list[i] - x_mean)**2 for i in range(n_pts)])
    s_y_2 = sum([(y_list[i] - y_mean)**2 for i in range(n_pts)])
    s_z_2 = sum([(z_list[i] - z_mean)**2 for i in range(n_pts)])
    coef_b1 = (s_z_2*s_xy - s_yz*s_xz) / (s_y_2*s_z_2 - s_yz**2)
    coef_b2 = (s_y_2*s_xz - s_yz*s_xy) / (s_y_2*s_z_2 - s_yz**2)
    coef_a = x_mean - coef_b1*y_mean - coef_b2*z_mean
    return(coef_a, coef_b1, coef_b2)

a, b1, b2 = bilin_reg(y_data, x1_data, x2_data)
print(f'y = {a:.2f} + {b1:.2f} * X1 + {b2:.2f} * X2')