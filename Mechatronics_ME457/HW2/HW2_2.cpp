/*
ME457 HW2 Problem 2

Let time be the x-axis or step size

Let pitch_rate be the reading in rad/s from the gyro
*/
#include <stdio.h>
#include <math.h>

float t_times[] = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9};
float g_data[] = {0.0, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.3, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, -0.1, -0.1, -0.2, -0.2, -0.3, -0.2, -0.1, -0.1};

int d_size = sizeof(g_data)/sizeof(g_data[0]);
float g_rates[d_size];

int main()
{
    for(int i=0; i < d_size; i++)
    {
        if (i == 0)
        {
            double hgt = t_times[i+1] - t_times[i];
            g_rates[i] = ((g_data[i] - g_data[i+1])/2) * hgt;
        }
    }
}
