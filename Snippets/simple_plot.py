from scipy.signal import TransferFunction as tf, impulse as imp, step as st

def simple_plot(ax_title, x_data, x_label, y_data, y_label, savename=None, fsave='.jpg'):
    '''
    Simple Plot: Accepts x and y data with label strings and optionally saves the figure
    in the format specified.
    ax_title : The main title at the top of the chart
    x_data : The array of x points
    x_label : The x-axis label
    y_data : The output from the x_data
    y_label : The y-axis label
    savename : Name of the file to save in the current directory (optional)
    fsave : File format for the plot save file (default is .jpg)
    '''
    # Imports matplotlib library
    import matplotlib.pyplot as plt
    # Create the plot
    plt.plot(x_data, y_data)
    # Set the title
    plt.title(ax_title)
    # x-axis label
    plt.xlabel(x_label)
    # y-axis label
    plt.ylabel(y_label)
    # save the figure if a save name is provided
    if savename:
        plt.savefig('{}{}'.format(savename,fsave), bbox_inches='tight')
    plt.show()

num = [1,]
den = [3, 21, 30]

tranny = tf(num, den)

imptime, impout = imp(tranny)
steptime, stepout = st(tranny)
simple_plot('Impulse Response problem 62', imptime, 'time (s)',\
                                        impout, 'Amplitude, x(t)',\
                                        'me_385_p2_62')
simple_plot('Step Response problem 63', steptime, 'time (s)',\
                                        stepout, 'Amplitude, x(t)',\
                                        'me_385_p2_63')


