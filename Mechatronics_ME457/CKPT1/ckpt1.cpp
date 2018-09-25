#include <iostream>
#include <cmath>

#define PI 3.14159265

double r2d = 180/PI;

using namespace std;

float butter2 (float f_c, float f_s, float dat_in, bool highpass)
{
    /* 
    2nd order butterworth filter for high or low pass data filtering

    this function is designed to be called within a computational loop
    and the idea is that it stores each input value to build and adjust
    the filter each time the function is called.

    f_c = cutoff frequency
    f_s = sampling frequency
    dat_in = value to be filtered
    highpass = if true, use high pass coefficients
    */
   // these coefficients are going to be the same
   float gamma = tan((PI*f_c)/f_s);
   float coef_d = pow(gamma, 2) + pow(2, 0.5)*gamma + 1;
   float a_1 = (2 * (pow(gamma, 2) - 1)) / coef_d;
   float a_2 = (pow(gamma, 2) - pow(2, 0.5)*gamma + 1)/coef_d;
   // set highpass or lowpass filtering coefficients
   float b_0, b_1, b_2;
   if (highpass == true)
   {
       b_0 = 1;
       b_1 = -2;
       b_2 = 1;
   } else {
       b_0 = (pow(gamma, 2)) / coef_d;
       b_1 = (2 * b_0) / coef_d;
       b_2 = b_0;
   }
   // hopefully these static declarations store the values
   // so we don't overwrite the coefficients each time the loop
   // hits this part. This code is untested, but is a proof of
   // concept.
   static float x_n1 = 0;
   static float x_n2 = 0;
   static float y_n1 = 0;
   static float y_n2 = 0;
   // calculate the new filtered value, then cycle variables
   float y_n = b_0*dat_in + b_1*x_n1 + b_2*x_n2 - a_1*y_n1 - a_2*y_n2;
   x_n2 = x_n1;
   x_n1 = dat_in;
   y_n2 = y_n1;
   y_n1 = y_n;
   return y_n;
}

