'''
Clay Freeman
Homework 1 McGrawHill
ME 306: Computer Aided Engineering
Dr. A. Stylianou

python scripts used to solve problems and assignments
'''


def num(n):
    # This is a short function that gets the number representation
    # for a number. 
    try:
        # If it is possible to return the input value as an integer,
        # return the integer
        return int(n)
    except ValueError:
        # Otherwise, if it is possible to return the value as a
        # float, then do that
        return float(n)
'''
def vel():
    # Chapter 1 Problem 6
    # Short script that accepts the initial time and final time
    # returns velocity using assumed parameters from problem

    # Gather user input
    # t_0, t_n, velocity
    # Error catching for the time variables are set up for integers
    while True:
        t_0 = input("Initial Time: ")
        if t_0.isdecimal():
            break
        print("Please Enter an Integer for Time.")
    while True:
        t_n = input("Final Time: ")
        if t_n.isdecimal():
            break
        print("Please Enter an Integer for Time.")
    # Some error catching for the float input on the velocity
    try:
        velocity = float(input("Initial Velocity (m/s): "))
    except ValueError:
        print("Please Enter a decimal number for Velocity.")



    # Set initial variables
    g = 9.81

    # These numbers were given in problem 6:
    mass = 80
    drag = 10

    ans = num(velocity) + ( g - ((drag * num(velocity)) / mass)) * (num(t_n) - num(t_0))
    print(ans)

vel()
'''
'''
def vel2():
    # Chapter 1 Problem 7:
    # 1.) find the velocity the first jumper reached in 9 seconds
    # 2.) determine the time it took for the second jumper to match
    #     this velocity
    
    # REQUIRES THE NUMPY LIBRARY TO WORK
    import numpy as np

    # Gather user inputs for each parachuter:

    try:
        mass_1 = float(input("First Parachuter Mass (kg) : "))
    except ValueError:
        print("Please Enter a decimal number for mass.")
    try:
        drag_1 = float(input("First Drag Coefficient (kg/s) : "))
    except ValueError:
        print("Please Enter a decimal number for drag.")
    try:
        mass_2 = float(input("Second Parachuter Mass (kg) : "))
    except ValueError:
        print("Please Enter a decimal number for mass.")
    try:
        drag_2 = float(input("Second Drag Coefficient (kg/s) : "))
    except ValueError:
        print("Please Enter a decimal number for drag.")
    try:
        time = float(input("Time in Freefall (s) : "))
    except ValueError:
        print("Please Enter a decimal number for drag.")

    # Set gravity

    g = 9.81

    # Calculate the velocity of the first parachuter after the freefall time
    # has ended.

    vel_1 = ((g * mass_1) / drag_1) * ( 1 - np.exp(((-1) * drag_1 * time) / mass_1))

    # Calculate the time it takes the second parachuter to reach the velocity
    # calculated in the previous line.

    t_2 = (-1) * (mass_2 / drag_2) * np.log(1 - ((vel_1 * drag_2) / (g * mass_2)))

    print("\nThe first parachutist reached " + str(vel_1) + " m/s in " + str(time) + " seconds.\n")
    print("\nThe second parachutist matched this speed in "+ str(t_2) + " seconds.\n")
    

vel2()
'''
'''
def vel3():
#    Chapter 1 Homework Assignment:
#    calculate the velocity using a step size
    g = 9.81
    try:
        mass = float(input("Parachuter Mass (kg) : "))
    except ValueError:
        print("Please Enter a decimal number for mass.")
    try:
        drag = float(input("First Drag Coefficient (kg/s) : "))
    except ValueError:
        print("Please Enter a decimal number for drag.")
    try:
        duration = int(input("End Velocity Time (s) : "))
    except ValueError:
        print("Please Enter an integer for time.")
    try:
        ssize = int(input("Step size : "))
    except ValueError:
        print("Please Enter a decimal number for step size.")

    def vel_cal(v_0, g, c, m, t, s):
        # This is a recursive function that takes all of the parameters for the problem
        # and returns the velocity. The idea is that this problem takes the form:
        # v(n) = v(n-1) + g - (c/m)*v(n-1)*(n-(n-1))
        # where: v(n) = velocity at this second
        #         n = this iteration
        #         c = drag coefficient
        #         m = object mass

        if t == 0:
            return 0
        else:
            ans = vel_cal(v_0, g, c, m, t-s, s) + g - (c/m) * vel_cal(v_0, g, c, m, t-s, s) * (t - (t-s))
            # print(ans)
            return ans
    

    value = vel_cal(0, g, drag, mass, duration, ssize)
    print(str(value))
vel3()
'''