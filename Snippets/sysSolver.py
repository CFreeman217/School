
import numpy as np
import scipy.optimize as spo
import math as math


def myFunction(z):
    # Known Values:
    rho = 999.1     # Density of Water
    mu = (1.138*pow(10,-3))  # Dynamic Viscosity constant
    sectionLength1 = 13    # Length of section 1 (meters)
    sectionLength2 = 35    # Length of section 2 (meters)
    lossCoeff_entrance = 0.5      # Loss coefficient, sharp entrance
    lossCoeff_collar = 0.46     # Loss coefficient, contraction
    pipeDiam1 = .1    # Large pipe diameter
    pipeDiam2 = .05   # Small pipe diameter
    area1 = (math.pi/4)*pipeDiam1**2 # Area of large pipe
    area2 = (math.pi/4)*pipeDiam2**2 # Area of small pipe
    alpha = 1   # Kinetic Energy Correction Factor (1 is negligible)
    eps = 0     # Roughness factor (0 for smooth plastic pipe)
    grav = 9.81    # Gravity
    # print(mu)
    # Set up system:
    vel_1 = z[0]  # Entrance Velocity
    vel_2 = z[1]  # Contraction Velocity
    fricFac_1 = z[2]  # Friction factor at region 1
    fricFac_2 = z[3]  # Friction factor at region 2
    headLoss = z[4]  # Head loss
    flowRate = z[5]  # Flow rate
    Re_1 = z[6] # Reynolds number section 1
    Re_2 = z[7] # Reynolds number section 2

    F = np.empty([8])

    # Functions
    F[0] = sectionLength1-(pow(vel_2,2))/(2*grav)-headLoss
    F[1] = (area2/area1)*vel_2-vel_1
    F[2] = ((fricFac_1*(sectionLength1/pipeDiam1)+lossCoeff_entrance)*((pow(vel_1,2)/(2*grav))))+((fricFac_2*(sectionLength2/pipeDiam2)+lossCoeff_collar)*((pow(vel_2,2))/(2*grav)))-headLoss
    F[3] = (vel_2*area2)-flowRate
    F[4] = (rho*pipeDiam1/mu)*vel_1-Re_1
    F[5] = (rho*pipeDiam2/mu)*vel_2-Re_2
    F[6] = ((-2)*(math.log(((eps/pipeDiam1)/3.7)+(2.51/(Re_1*np.sqrt(fricFac_1))))))-(1/np.sqrt(fricFac_1))
    F[7] = ((-2)*(math.log(((eps/pipeDiam2)/3.7)+(2.51/(Re_2*np.sqrt(fricFac_2))))))-(1/np.sqrt(fricFac_2))

    return F

zGuess = np.array([.75,4.75,.01,.01,15,.005,66000,160000])

z = spo.fsolve(myFunction,zGuess)

print(z)