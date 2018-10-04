/*
ME457 HW2 Problem 2
*/
// initialize libraries
#include <stdio.h>
#include <iostream>
#include <string>
// define constants
#define PI 3.14159265

int main()
{
    // Initial pitch reading
    double i_pitch = 0;
    // first gyrometer reading
    double g_point1 = 0;
    // second gyrometer reading
    double g_point2 = 0.1;
    // first time point
    double t_point1 = 0;
    // second time point
    double t_point2 = 0.1;
    // current pitch calculation using trapezoidal numeric integration method
    double current_pitch = i_pitch + ((t_point2 - t_point1)*-1) * ((g_point1 + g_point2)/2) * (180/PI);

    std::cout << "For initial pitch reading : " << i_pitch << std::endl;
    std::cout << "Initial gyrometer reading : " << g_point1 << std::endl;
    std::cout << "Final gyrometer reading : " << g_point2 << std::endl;
    std::cout << "Initial time reading : " << t_point1 << std::endl;
    std::cout << "Final time reading : " << t_point2 << std::endl;
    std::cout << "Calculated pitch output : " << current_pitch << std::endl;
    


}
