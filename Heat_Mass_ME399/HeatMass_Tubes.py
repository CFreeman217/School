import os, re, numpy as np 
import matplotlib.pyplot as plt 

c2f = lambda x : (9/5)*x + 32
f2c = lambda x : (x-32)*(5/9)

f_wind = 10 # mph
m_wind = f_wind/.44704
a_temp_f = 90 # degrees F
s_temp_f = 74 # degrees F
s_t = 19 # mm, Transverse (vertical) spacing
s_l = 19 # mm, Longitudinal (horizontal) spacing
n_rows = 6 # number of tubes the air passes over to exchange temp
t_diam = 40 # mm, Tube diameter
t_leng = 1000 #mm, Tube length


a_temp_c = f2c(a_temp_f)
s_temp_c = f2c(s_temp_f)
t_bulk = (a_temp_c + s_temp_c)/2
Pr_a = 0.71 # Prandtl number for air at free stream - Appendix 2
Pr_s = 0.71 # Prandtl number at surface - Appendix 2


t_s = f2c(air_temp)
t_a = f2c(surf_temp)
def inline(Re_d):
    Nu_d = (0.021*Re_d**(.84))*((Pr_a**0.36)*((Pr_a/Pr_s)**0.25))

def staggered(Re_d):
    Nu_d = 