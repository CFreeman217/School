import os
currentDir = os.getcwd()

import sys
sys.path.append(currentDir)

import turtle as *


    
def h_dimension(value,endX,height):
    startX = round(turtle.xcor(),2)
    startY = round(turtle.ycor(),2)
    endY = startY + height
    mag = (abs(endX-startX))/value
    bigSpace = mag * 15
    littleSpace = mag * .05
    drawDistance = endX - startX

    turtle.mode("standard")
    turtle.setheading(90)
    turtle.pencolor("blue")
    turtle.pensize(3)

    pd();goto(startX,endY);pu()
    

    cb_Y = endY - littleSpace


