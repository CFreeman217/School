/*
ME457 HW2 Problem 1

Let pitch axis be the x-axis where the nose is along the positive y-axis and the positive z-axis is down.

Let the variable accels hold the three accelerometer readings provided to the program in m/s^2

*/
// Load nessecary libraries
#include <stdio.h>
#include <math.h>

// Define pi
#define PI 3.14159265
// Generate the constant to convert radians to degrees
double r2d = 180/PI;

// Input an array of floats to hold accelerometer readings
float accels[] = {1.0, 1.5, 10.81};

int main()
{
      // gather acceleration
      double ax = accels[0];
      double ay = accels[1];
      double az = accels[2] - 9.81;

      // calculate pitch, roll and yaw
      double pitch = atan2(ax, -az) * r2d;
      double roll = atan2(ay, -az) * r2d;
      double yaw = atan2(ay, ax) * r2d;


      // print the results
      printf(" Pitch = %f , Roll = %f, Yaw = %f \n", pitch, roll, yaw);
      return 0;
}