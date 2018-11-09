## module prob5_17
''' Test case for false position method for finding roots of functions'''
from false_position import false_position

def main():
    '''
    Problem 5-17 : Estimating volume of spherical tank
    False Position Method Results :

    Approximated Value : 2.0239040641919983
    Function Output : -0.07591309089005449
    Estimated Error : 0.018444085092809506
    Iteration Count : 3
    '''
    from math import pi
    R = 3 # meters - Radius of tank
    V = 30 # m^3 - Volume to estimate
    m_it = 3 # Iteration limit
    # Volume of sphere minus estimation volume (find zero for this function)
    f = lambda h : pi * h ** 2 * (3*R - h)/3 - V
    h_low = 0 # Lower guess
    h_high = R # Upper guess

    false_position(f, h_low, h_high, 0, m_it)
main()