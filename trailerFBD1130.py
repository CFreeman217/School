# -*- coding: utf-8 -*-
import datetime
from datetime import datetime, date, time

import turtle
from turtle import *

import tkinter
from tkinter import *

now = datetime.now()

"""
96 inch maximum from tire to tire. 
https://ops.fhwa.dot.gov/freight/publications/size_regs_final_rpt/
Shafts come 94.25" in length. This leaves about 7/8" for each side
in tire swell.
https://www.google.com/shopping/product/1154601681497844215?lsf=seller:8049,store:7035007347242396795&prds=oid:8570072897603788124&q=self+axle+length&hl=en&ei=2KIdWoj9Hoq9jwTV-qLoCQ&lsft=gclid:EAIaIQobChMI_7LYsOvh1wIV1brACh1dBwoHEAQYASABEgI6rPD_BwE

If load is 2500 lbs then design shaft for 3500lbs

6 lug wheels can fit axle capacity of 3500-6000lbs
https://www.etrailer.com/question-50942.html


Trailer tongue weight should be between 9-15%: 10% goal

Measurements given from assuming a 20' length

Steel Density is between 404 and 503 lb/ft^3

[boat wt + engine wt + (Fuel self.Capacity)*7lbs/gal + (Water self.capacity)]*1.1
http://www.boattraileroutlet.com/choose-the-correct-self

https://www.etrailer.com/question-105291.html

1.) Get total weight from wheels (wheel weight)
2.) Get tongue weight
3.) Distance from tongue to axle
4.) Get Total Weight

http://www.truckinginfo.com/article/print/story/2013/02/calculate-true-self.capacity-before-buying-your-next-self-part-three.aspx
Able to use design factor between 1.8 and 2.5

Automotive design factor standard is to use 3 - Mechanical Analysis and Design, Burr, Arthur H. Prentice Hall 1995 (cannot find)
"""
class trailer:
    def __init__(self):
        
        # self.totalLoad = 2500
        # self.boatLength = 20
        # self.trailDist = 4.5
        self.tireDiam = 20.5
        self.slProp = .66
        self.smDist = .66
        self.twProp = .1
        # self.FOS = 1.7
        
        self.totalLoad = float(input("\nEnter Load Weight (lbs)=  "))
        self.boatLength = float(input("\nEnter Boat Length (feet) =  "))
        self.trailDist = float(input("\nEnter distance from tip of bow to towing vehicle (feet) =  "))
        # self.tireDiam = float(input("\nEnter tire outer diameter (inch) =  "))
        # self.slProp = float(input("\nEnter proportion of boat length in contact with skids (.5 to .75) =  "))
        # self.smDist = float(input("\nSkid mount spacing proportion (between .5 and .75) =  "))
        # self.twProp = float(input("\nTongue Weight proportion (.09-.15, use .10) =  "))
        self.FOS = float(input("\nEnter Factor of Safety (1.7 - 2.5) =  "))
        
        self.capacity = ((self.totalLoad) * (self.FOS))
        self.skidMountLoad = self.capacity/2
        self.trailLength = (((self.boatLength) + (self.trailDist)) * 12)
        self.skidLength = ((self.boatLength) * (self.slProp) * 12)
        self.mountSpacing = (self.skidLength * (self.smDist))
        self.skidMount1 = ((self.skidLength - self.mountSpacing)/ 2)
        self.skidMount2 = (self.skidLength - self.skidMount1)
        self.trailSkidMount1 = (self.trailLength - self.skidLength + self.skidMount1)
        self.trailSkidMount2 = (self.trailLength - self.skidLength + self.skidMount2)
        self.loadCOG = (self.trailLength - (self.skidLength/2))
        self.axleDist = (self.loadCOG / (1 - (self.twProp)))
        self.axleLoad = (self.capacity * (1- (self.twProp)))
        self.tongueLoad = (self.capacity * (self.twProp))

    def draw_trailer(self):
        display = turtle.Screen()
        mode("standard")
        speed(10)

        # Trailer Geometry
        pensize(3);pencolor("black")

        # Bar
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(180)
        pd();fd(self.trailLength);rt(90);fd(4);rt(90);fd(self.trailLength);rt(90);fd(4);pu()
        
        # Tire
        rt(180);fd(6);lt(90);fd((self.axleDist));rt(90);fd((self.tireDiam));lt(90);pd();begin_fill();circle((self.tireDiam));end_fill();pu()
        
        # Supports
        home();pu();rt(180);pu();fd(self.trailLength/2);rt(180);fd(self.trailSkidMount1);rt(180)
        pd();fd(2);rt(90);fd((self.tireDiam)+3);rt(90);fd(4);rt(90);fd((self.tireDiam)+3);rt(90);fd(2);pu()
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(180);fd(self.trailSkidMount2);rt(180)
        pd();fd(2);rt(90);fd((self.tireDiam)+3);rt(90);fd(4);rt(90);fd((self.tireDiam)+3);rt(90);fd(2);pu()
        
        # Skids
        home();pu();fd((self.trailLength)/2);lt(90);fd((self.tireDiam)+3)
        pd();fd(4);lt(90);fd(self.skidLength);lt(90);fd(4);lt(90);fd(self.skidLength);pu()

        # Ends
        pu();home();rt(180);fd(self.trailLength/2);rt(180);fd((self.trailDist)* 12);lt(180)
        pd();fd(2);rt(90);fd(2.25*(self.tireDiam));rt(90);fd(2);pu();rt(90);fd(5);lt(90);pd();circle(7);pu();lt(90);fd(5);rt(90)
        pd();fd(2);rt(90);fd(2.25*(self.tireDiam));rt(90);fd(2);pu()
        
        
        # Dimensions
        pencolor("blue")
        
        # Upright Lines
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(10)
        pd();fd(320);pu();rt(90);fd(self.trailLength);rt(90)
        pd();fd(280);pu()
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(50);rt(90);fd(self.trailSkidMount2);lt(90)
        pd();fd(240);pu()
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(50);rt(90);fd(self.axleDist);lt(90)
        pd();fd(200);pu()
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(50);rt(90);fd(self.trailSkidMount1);lt(90)
        pd();fd(160);pu()
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(50);rt(90);fd(self.trailLength-self.skidLength);lt(90)
        pd();fd(120);pu()
        
        # Dimension bars and labels
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(310);rt(90);pd();fd(25);pu();fd(15)
        write(round(self.trailLength,2),font=("Arial",10,"bold"));fd(35);pd();fd(self.trailLength-75);pu()
        
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(270);rt(90);pd();fd(25);pu();fd(15)
        write(round(self.trailSkidMount2,2),font=("Arial",10,"bold"));fd(35);pd();fd(self.trailSkidMount2-75);pu()
        
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(230);rt(90);pd();fd(25);pu();fd(15)
        write(round(self.axleDist,2),font=("Arial",10,"bold"));fd(35);pd();fd(self.axleDist-75);pu()
        
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(190);rt(90);pd();fd(25);pu();fd(15)
        write(round(self.trailSkidMount1,2),font=("Arial",10,"bold"));fd(35);pd();fd(self.trailSkidMount1-75);pu()
        
        home();pu();rt(180);pu();fd((self.trailLength)/2);rt(90);fd(150);rt(90);pd();fd(25);pu();fd(15)
        write(round((self.trailLength-self.skidLength),2),font=("Arial",10,"bold"));fd(35);pd();fd((self.trailLength-self.skidLength)-75);pu()
        
        # Forces
        pencolor("red")

        # Up Arrow
        home();pu();rt(180);pu();fd((self.trailLength)/2);lt(90);fd(15)
        pd();rt(30);fd(10);lt(120);fd(10);lt(120);fd(10);lt(150);fd(100);pu();fd(15);lt(90)
        write(round(self.tongueLoad,2),font=("Arial",10,"bold"))
        
        # Down Arrow
        home();pu();rt(180);pu();fd((self.trailLength)/2);lt(90);fd(15);lt(90);fd(self.trailSkidMount1);rt(90)
        pd();fd(100);rt(150);fd(10);rt(120);fd(10);rt(120);fd(10);lt(30);pu();fd(15);lt(90)
        write(round(self.skidMountLoad,2),font=("Arial",10,"bold"))

        # Up Arrow
        home();pu();rt(180);pu();fd((self.trailLength)/2);lt(90);fd(15);fd((self.tireDiam));lt(90);fd(self.axleDist);rt(90)
        pd();rt(30);fd(10);lt(120);fd(10);lt(120);fd(10);lt(150);fd(100);pu();fd(15);lt(90)
        write(round(self.axleLoad,2),font=("Arial",10,"bold"))

        # Down Arrow
        home();pu();rt(180);pu();fd((self.trailLength)/2);lt(90);fd(15);lt(90);fd(self.trailSkidMount2);rt(90)
        pd();fd(100);rt(150);fd(10);rt(120);fd(10);rt(120);fd(10);lt(30);pu();fd(15);lt(90)
        write(round(self.skidMountLoad,2),font=("Arial",10,"bold"))

        file_name = ("TrailerFBD_Graph_" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.second))
        ht()
        display.getcanvas().postscript(file=file_name)
        display.exitonclick()

    def draw_axle(self):

        self.wheelWidth = float(input("Enter Wheel width for 98 in. hub to hub zero offset centered: (between 4-6in) "))
        self.axleLength = 98
        self.axleMag = float(input("Enter Magnification factor"))
        rise = 2
        halfAxle = self.axleLength/2
        halfWheel = self.wheelWidth/2
        display = turtle.Screen()
        mode("standard")
        speed(10)  
        pensize(3);pencolor("black")
        pu();home();rt(180);fd(halfAxle);rt(90);fd(rise)
        pd();rt(90);fd(halfWheel);lt(90);fd(rise);rt(90);fd(self.wheelWidth);lt(90);fd(rise);rt(90);fd(self.axleLength-(self.wheelWidth*3))
        rt(90);fd(rise);lt(90);fd(self.wheelWidth);rt(90);fd(rise);lt(90);fd(halfWheel);rt(90);fd(2*rise)
        rt(90);fd(halfWheel);lt(90);fd(rise);rt(90);fd(self.wheelWidth);lt(90);fd(rise);rt(90);fd(self.axleLength-(self.wheelWidth*3)) 
        rt(90);fd(rise);lt(90);fd(self.wheelWidth);rt(90);fd(rise);lt(90);fd(halfWheel);rt(90);fd(2*rise);pu()
        display.exitonclick()

trailer_1 = trailer()
# print(trailer_1.__dict__)
trailer_1.draw_trailer()