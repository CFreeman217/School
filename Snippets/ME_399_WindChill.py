import matplotlib # Import library used for plotting figures
matplotlib.use('TkAgg') # Create reference for UI
# Create a path for matplotlib to interact with the canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Numpy is used for math processing and generating surfaces
import numpy as np
# Reference to generate the figure
import matplotlib.pyplot as plt
# Reference for 3D Axes
from mpl_toolkits.mplot3d import Axes3D
# Color mapping for labeling the surface
from matplotlib import cm
# Import UI library. For this project we are using tkinter
import tkinter as Tk
# Import access to the system for exiting the program
import sys

# Set up a function to help the UI exit the interface
def destroy(e):
    sys.exit()

def c2f(temp):
    ans = ((9/5) * temp) + 32
    return ans

# Defines the base window element
root = Tk.Tk()
# Sets the title in the grey box at the top of the window
root.wm_title("ME 399: Heat and Mass Transfer")

# Generate a figure
fig = plt.figure()
# Create a set of axes at a 3d projection angle
ax = fig.add_subplot(111, projection='3d')
# Create a  range of values for wind speed
windSpeed = np.arange(0,100,1)
# Create a range of values for temperature
f_min = -40
f_max = 40
temp_F = np.arange(f_min, f_max,1)
c_min = (f_min - 32) * (5/9)
c_max = (f_max - 32) * (5/9)
temp_C = np.arange(c_min, c_max)
# Generate a mesh for velocity and temperature to produce a surface
V, T = np.meshgrid(windSpeed, temp_C)
# Generate values nessecary to calculate windchill
windChill = 35.74 + (0.6215 * c2f(T)) - (35.75 * (V ** (0.16))) + (0.4275 * c2f(T) * (V ** (0.16)))
# Set the Z values as windchill
Z = (windChill - 32) * (5/9)
# Plot the axis surface (X, Y, Z) setting the color map, line width, and anti-aliasing
surf = ax.plot_surface(V, T, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
# Produce a color bar as a key to help describe the plot
key = fig.colorbar(surf, shrink=0.5, aspect=5)

# Label axes and title
ax.set_xlabel('Wind Speed (mph)')
ax.set_ylabel('Temperature (C)')
ax.set_zlabel('Wind Chill Temp(C)')
ax.set_title('Wind Chill for All Wind Speed and Temperature')

# Places the figure in the canvas
canvas = FigureCanvasTkAgg(fig, master=root)
# Draws the window with figure
canvas.show()
# Create the 
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
