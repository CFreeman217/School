import datetime
from datetime import datetime, date, time
now = datetime.now()

import turtle
from turtle import *

class bearing:
    def __init__(self):
        return

class shaft:
    def __init__(self):
        return

def dimension(value,cb_height,cb_width,bigSpace,smSpace):
    pu()
    setheading(0);lt(90);fd(smSpace);pd();fd(cb_height);pu();rt(180);fd(bigSpace);lt(90)
    pd();fd((cb_width/2)-bigSpace);pu();fd(bigSpace/2);write(value,font=("Arial",15,"bold"));fd((3*bigSpace)/2);pd();fd((cb_width/2)-bigSpace);pu()
    lt(90);fd(bigSpace);rt(180);pd();fd(cb_height);pu()

def uparrow(value,ldr_hgt):
    pu();setheading(0);rt(90)
    pd();rt(30);fd(10);lt(120);fd(10);lt(120);fd(10);lt(150);fd(ldr_hgt);pu();fd(25);lt(90)
    write(value,font=("Arial",15,"bold"))
    
def dnarrow(value,ldr_hgt):
    pu();setheading(0);rt(90)
    pd();fd(ldr_hgt);rt(150);fd(10);rt(120);fd(10);rt(120);fd(10);lt(30);pu();fd(25);lt(90)
    write(value,font=("Arial",15,"bold"))

def inch_2_foot(in_inch):
    out_feet, footfrac = divmod(in_inch/12,1)
    out_inch = in_inch - (out_feet * 12)
    out_string = " " + str(out_feet) + "-ft.  " + str(out_inch) + "-in. "
    return out_string

def mm_2_inch(in_mm):
    out_in = in_mm * 0.03937
    return out_in

def lb_2_N(in_lbs):
    out_N = in_lbs * 4.44822


def gatherVariables():
    # bearing.bore = float(input("Enter a Bore Diameter (mm) : "))
    bearing.bore = (65)
    # bearing.OD = float(input("\nEnter an Outer Diameter (mm) : "))
    bearing.OD = (120)
    # bearing.width = float(input("\nEnter bearing width (mm) : "))
    bearing.width = (23)
    # bearing.spacing = float(input("\nEnter space between bearings (in) :"))
    bearing.spacing = 2
    # bearing.distance = float(input("\nInner bearing to frame mount (in) :"))
    bearing.distance = 5
    # bearing.c10 = float(input("\nEnter a C_10 value from table 11-3 (kN) : "))
    bearing.c10 = 76.5
    shaft.small = bearing.bore
    shaft.big = 75
    shaft.load = 1687.5
    shaft.loadLoc = bearing.distance + bearing.spacing
    bearing.load2 = (shaft.load*(bearing.distance+bearing.spacing))/bearing.spacing
    bearing.load1 = bearing.load2-shaft.load



def setup_turtle():
    display = turtle.Screen()

    mode("standard")
    speed(0)
    home()

def drawBearing(mag):
    pensize(3);pencolor("black")
    overhang = 1*mag
    bearing.drawBore = mm_2_inch(bearing.bore) * mag
    bearing.drawOD = mm_2_inch(bearing.OD) * mag
    bearing.drawWidth = mm_2_inch(bearing.width) * mag
    bearing.drawSpacing = bearing.spacing * mag
    bearing.drawDistance = bearing.distance * mag
    bearing.drawShoulder = (mm_2_inch(shaft.big) * mag - bearing.drawBore)/2
    home();pd();lt(90);fd(bearing.drawBore);rt(90);fd(overhang+(2*bearing.drawWidth)+bearing.drawSpacing);lt(90)
    fd(bearing.drawShoulder);rt(90);fd(20*mag);pu()
    home();pd();fd(overhang+(2*bearing.drawWidth)+bearing.drawSpacing);rt(90);fd(bearing.drawShoulder);lt(90)
    fd(20*mag);pu()
    
    home();fd(overhang);rt(90);pd();fd((bearing.drawOD-bearing.drawBore)/2);lt(90);fd(bearing.drawWidth);lt(90)
    fd(bearing.drawOD);lt(90);fd(bearing.drawWidth);lt(90);fd(bearing.drawOD);pu()
    home();fd(overhang+bearing.drawSpacing+bearing.drawWidth);rt(90);pd();fd((bearing.drawOD-bearing.drawBore)/2);lt(90);fd(bearing.drawWidth);lt(90)
    fd(bearing.drawOD);lt(90);fd(bearing.drawWidth);lt(90);fd(bearing.drawOD);pu()

    pencolor("blue")
    home();lt(90);fd(bearing.drawBore);fd(mag);pd()
    dimension(1,15*mag,overhang+bearing.drawWidth/2,3*mag,1*mag)
    exitonclick()


setup_turtle()
gatherVariables()
drawBearing(10)