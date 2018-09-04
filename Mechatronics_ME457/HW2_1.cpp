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
float accels[] = {0.0, 0.0, 9.81};

int main()
{
      // gather acceleration
      double ax = accels[0];
      double ay = accels[1];
      double az = accels[2] - 9.81;

      // calculate pitch, roll and yaw
      double pitch = atan( ax / (sqrt(pow(ay,2.0) + pow(az, 2.0))));
      double roll = atan( ay / (sqrt(pow(ax, 2.0) + pow(az, 2.0))));
      //double yaw = atan( az / (sqrt(pow(ax, 2.0) + pow(ay, 2.0))));
      double yaw = atan((sqrt(pow(ax, 2.0) + pow(ay, 2.0))) / az);

      // convert to degrees
      pitch *= r2d; roll *= r2d; yaw *= r2d;

      // print the results
      printf(" Pitch = %f , Roll = %f, Yaw = %f \n", pitch, roll, yaw);
      return 0;
}