import sys
import math
import numpy as np
import time

# WGS 84
f = 1 / 298.257223563
e_2 = 2 * f - f**2
a = 6378137.  # SMA


# https://gssc.esa.int/navipedia/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion 
def xyz2llh(pos):
    # [phi, lambda, h]
    x, y, z = pos
    lam = math.atan(y/x)

    p = math.sqrt(x**2 + y**2)

    # inital calculation
    phi = math.atan(z/((1-e_2) * p))
    h = 0

    for i in range(10):
        N = a/(math.sqrt(1-e_2*((math.sin(phi))**2)))
        h = p/(math.cos(phi)) - N
        denom = 1-e_2*N/(N+h)
        phi = math.atan(z/(denom*p))

    return np.array([phi, lam, h])