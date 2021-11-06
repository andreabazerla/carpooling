import numpy as np
import math

def cartesian_2_polar(cartesian_coordinate):
    x = cartesian_coordinate[0]
    y = cartesian_coordinate[1]

    rho = np.sqrt(x**2 + y**2)

    if (x == 0):
        if (y > 0):
            phi = np.pi/2
        elif (y < 0):
            phi = 3*np.pi/2
        else:
            phi = 0
    else:
        if (y >= 0):
            phi = np.arctan2(y, x)
        else:
            phi = np.arctan2(y, x) + 2*np.pi
    
    return (rho, math.degrees(phi))

def polar_2_cartesian(polar_coordinate):
    rho = polar_coordinate[0]
    phi = polar_coordinate[1]

    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    
    return (x, y)