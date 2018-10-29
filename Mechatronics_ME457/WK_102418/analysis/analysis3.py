import os, math
import numpy as np, matplotlib.pyplot as plt
# Start and end plot data points
s_plot = 905
e_plot = 4005

def butter2(f_c, f_s, in_list, highpass=False):
    '''
    2nd Order Butterworth Filter:
    f_c = cutoff frequency - adjust this to change amount of filtering
    f_s = sampling frequency - determined by the sampling rate of the dataset
    in_list = list of collected data points to be filtered
    '''
    gam = math.tan((math.pi*f_c)/f_s)
    coef_d = gam**2 + (2**0.5)*gam + 1
    a_1 = (2 * (gam**2 - 1)) / coef_d
    a_2 = (gam**2 - (2**0.5)*gam + 1)/coef_d
    if highpass:
        b_0 = 1
        b_1 = -2
        b_2 = 1
    else:
        b_0 = (gam**2) / coef_d
        b_1 = (2*b_0) / coef_d
        b_2 = b_0
    x_n1 = 0
    x_n2 = 0
    y_n1 = 0
    y_n2 = 0
    out_list = []
    for value in in_list:
        y_n = b_0*value + b_1*x_n1 + b_2*x_n2 - a_1*y_n1 - a_2*y_n2
        out_list.append(y_n)
        x_n2 = x_n1
        x_n1 = value
        y_n2 = y_n1
        y_n1 = y_n

    return out_list

def tune_tangent(d_l, tau, psi_ss, d_sig):
    '''
    Tangent tuning method:
    d_l = time from step signal initiation to when the device begins to respond to the input
    tau = intersection of final steady state value and tangent line to sloped region for controller
    psi_ss = total change in yaw rate during baseline test
    d_sig = chang in input signal from zero to final value
    '''
    k_tot = psi_ss/d_sig
    k_p = 1.2*(tau/ (k_tot*d_l))
    k_i = k_p / (2 * d_l)
    k_d = (k_p * d_l) / 2
    return k_p, k_i, k_d


for file_name in os.listdir('.'):
    if file_name == 'clay_try_1529_Feb_18_06_22-0.csv':
        d_time, yaw, signal, filt_yaw = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 26, 30, 31),)
        # Convert time to seconds
        d_time /= 1000000
        # After plotting several times and looking at the graphs
        # Set start signal and response to signal times
        sig_start = 33.75
        resp_start = 34.5
        psi_steady = 7 # Raw data change in yaw rate in response to input
        # Delta L to calculate gains
        delt_l = resp_start - sig_start
        t_int = 39.6 # Tau intercept for determining the slope line and tau
        tau_T = t_int - sig_start # Tau for tangent gain method
        # Draw sloped line to fit 
        slopeline = lambda x : (x-t_int)*(-0.017)
        newline = [slopeline(i) for i in d_time]
        # Butterworth filtering on gyro output data that came in with lots of noise
        filt_yaw2 = butter2(1,100,filt_yaw)
        # Adjust and scale the filtered yaw data to overlay with the signal input
        filt_yaw2 = [(i/80)+.13 for i in filt_yaw2]
        # Plot signal and yaw data
        plt.plot(d_time[s_plot:e_plot], signal[s_plot:e_plot], label='Signal')
        plt.plot(d_time[s_plot:e_plot], filt_yaw2[s_plot:e_plot], label='Yaw Measured (Scale = 1:80)')
        plt.plot(d_time[s_plot:e_plot], newline[s_plot:e_plot], c='r', linestyle=':')
        plt.title('Yaw and Response\nOpen Loop Gain Tuning Tangent Method')
        plt.xlabel('time (s)')
        plt.ylabel('Yaw Rate (Rad/s)')
        plt.axvline(x=sig_start,c='r',linestyle=':')
        plt.axvline(x=resp_start,c='r',linestyle=':')
        kP, kI, kD = tune_tangent(delt_l, tau_T, psi_steady, 0.1)
        plt.text(19, 0.06, r'K$_p$ = {:1.6f}'.format(kP),{'color':'k', 'fontsize':12, 'ha':'left', 'bbox': dict(boxstyle='round', fc='w', ec='w',pad=0.2)})
        plt.text(19, 0.05, r'K$_i$ = {:1.6f}'.format(kI),{'color':'k', 'fontsize':12, 'ha':'left', 'bbox': dict(boxstyle='round', fc='w', ec='w',pad=0.2)})
        plt.text(19, 0.04, r'K$_d$ = {:1.6f}'.format(kD),{'color':'k', 'fontsize':12, 'ha':'left', 'bbox': dict(boxstyle='round', fc='w', ec='w',pad=0.2)})
        plt.ylim(-0.03,0.13)
        plt.grid(b=True, which='both')
        # plt.grid(b=True, which='major', axis='both')
        plt.legend(loc=3)
        plt.savefig('ckpt_fig1.png'.format(file_name[:-4]), bbox_inches='tight')
        plt.show()
