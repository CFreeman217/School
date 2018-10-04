#! usr/bin/env python

from scipy import signal
import numpy as np
 
def prob3_15a():
    arrA = np.array([[0, 1, 5, 0],[0, 0, 1, 0],[0, 0, 0, 1],[-7, -9, -2, -3]])
    arrB = np.array([[0],[5],[8],[2]])
    arrC = np.array([1, 3, 6, 6])
    arrD = np.array([0])

    sys = signal.StateSpace(arrA, arrB, arrC, arrD).to_tf()
    print('\n ~~ PROBLEM 3-15a ~~ \n')
    print(sys.num)
    print('-'*30)
    print(sys.den)
    

def prob3_15b():
    arrA = np.array([[ 3, 1,  0,  4, -2],
                     [-3, 5, -5,  2, -1],
                     [ 0, 1, -1,  2,  8],
                     [-7, 6, -3, -4,  0],
                     [-6, 0,  4, -3,  1]])
    arrB = np.array([[2],
                     [7],
                     [8],
                     [5],
                     [4]])
    arrC = np.array([1, -2, -9, 7, 6])
    arrD = np.array([0])

    sys = signal.StateSpace(arrA, arrB, arrC, arrD).to_tf()
    print('\n ~~ PROBLEM 3-15b ~~ \n')
    print(sys.num)
    print('-'*30)
    print(sys.den)

prob3_15a()

prob3_15b()

