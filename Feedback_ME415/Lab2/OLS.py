import os
import numpy as np, matplotlib.pyplot as plt
from openpyxl import load_workbook

freqs = []
M_vals = []

for file_name in os.listdir('.'):
    if file_name == 'Data.xlsx':
        wkbk = load_workbook(file_name)
        wkst = wkbk.active
        for row in range(2,16):
            cell_name = f'F{row}'
            freqs.append(wkst[cell_name].value)
            cell_name = f'G{row}'
            M_vals.append(wkst[cell_name].value)
    if file_name == 'M_values_new2.csv':
        f_val, m_val = np.loadtxt(file_name,
                                    delimiter=',',
                                    unpack=True,
                                    skiprows=1,
                                    usecols=(0,1))
print(freqs)
a_i = 250000
b_i = 3000
c_i = 200

model = lambda w, a, b, c : (a / (np.sqrt(b*w - w**3)**2 + (a - c*w**2)**2))
dM_da = lambda w, a, b, c : (w**2*(-1*a*c + (w**2 - b)**2 + c**2*w**2)) / (((a - c*w**2)**2 + (w**3 - b*w)**2)**(1.5))
dM_db0 = lambda w, a, b, c : ((a*w**2*(w**2 - b)) / (((a - c*w**2)**2 + (w**3 - b*w)**2)**(3/2)))
dM_db1 = lambda w, a, b, c : ((a*w**2*(a - c*w**2)) / (((a - c*w**2)**2 + (b*w - w**3)**2)**(3/2)))

y_model = []
y_icol = []
for i in range(5):
    y_irow = []
    for f in range(len(freqs)):
        a_est = dM_da(freqs[f], a_i, b_i, c_i)
        b0_est = dM_da(freqs[f], a_i, b_i, c_i)
        b1_est = dM_da(freqs[f], a_i, b_i, c_i)

        current = model(freqs[f], a_est, b0_est, b1_est)
        y_model.append(current)
        y_irow.append(current - m_val[f])
    y_icol.append(y_irow)

    H_val = np.array([a_est, b0_est, b1_est])
    params = np.linalg.inv(H_val.T*H_val)*(H_val.T*np.array(y_irow))
    print(params)


# clear all;close all;clc;

# % IMPORT DATA HERE -------------------------------------------------------%

# %load('Experiment1') % data from a mat file
# data = xlsread('Data'); % data from xls file
# %file = xlsread('FREQ_30'); % data from xls file

# x = data(5,:)'; 
# y_raw = data(:,5)';
# frq = data(:,4);





# M = data(:,2);
# t = 0:1:length(M)-1;



# n_max = 3;                          % Maximum model order to estimate             % Output data
# N = length(y_raw);                      % number of data points
# time = 1:1:N;

# %-------------------------------------------------------------------------%



# %MAIN---------------------------------------------------------------------%

# % Intializing parameters and bias
# params = zeros(n_max+1, n_max);
# bias = ones(1,N)';

# % Model structure




# A = 250000;
# B1 = 200;
# B0 = 3000;

   
# for j = 1:5





    

# %     p1a=((1/(sqrt((A-B1.*frq.^2).^2 + (B0.*frq - frq.^3).^2))) - ((A*(A-B1.*frq.^2))/(((A-B1.*frq.^2).^2 +(B0.*frq - frq.^3).^2).^(3/2))));
# %     p2a= ((A.*frq.^2.*(A - B1.*frq.^2))/((A - B1.*frq.^2).^2 + (B0.*frq - frq.^3).^2).^(3/2));
# %     p3a = ((-A.*frq.*(B1.*frq-frq.^3)/((A - B1.*frq.^2).^2 + (B0.*frq - frq.^3).^2).^(3/2)));
# for i =1:14
    
#     p1a(i)=((1/(sqrt((A-B1*frq(i)^2)^2 + (B0*frq(i) - frq(i)^3)^2))) - ((A*(A-B1*frq(i)^2))/(((A-B1*frq(i)^2)^2 +(B0*frq(i) - frq(i)^3)^2)^(3/2))));
#     p2a(i) = ((A*frq(i)^2*(A - B1*frq(i)^2))/((A - B1*frq(i)^2)^2 + (B0*frq(i) - frq(i)^3)^2)^(3/2));
#     p3a(i) = ((-A*frq(i)*(B1*frq(i)-frq(i)^3)/((A - B1*frq(i)^2)^2 + (B0*frq(i) - frq(i)^3)^2)^(3/2)));

    
#     ym(i) = (A/sqrt((B0*frq(i)-frq(i)^3)^2 + (A-B1*frq(i)^2)^2));
#     yi(i) = y_raw(i) - ym(i);
    
# end
#     H = [p1a' p2a' p3a'];


#     params= (H'*H)\(H'*yi') % Estimated parameters


#     A = A + params(1,1)
#     B1 = B1 + params(2,1)
#     B0 = B0 + params(3,1) 

#     AA(j) = A;
#     B11(j) = B1;
#     B00(j) = B0;
#     k = j



# end

# % for i=1:14
# %     
# % ym(i) = (A/sqrt((B0*frq(i)-frq(i)^3)^2 + (A-B1*frq(i)^2)^2));
# % 
# % end


# figure(1)
# plot(frq,yi,frq,y_raw,'--')
# figure(2)
# plot(frq,ym)
# figure(3)
# plot(frq,y_raw)
