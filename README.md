# Advitiy-Control-Model

main.py : contains main loop of the simulation

constants.py : contains all constants
frames.py : contains frame conversions
qnv.py : contains functions of attitude kinematics
satellite.py : contains declaration of satellite object

Python Code to use IGRF

from pyigrf12 import runigrf12
z1 = 0
z2 = 1
B = runigrf12(day,z1,z2,height,lat,lon)
#B : in nano tesla in NED frame. first 3 components are Bn, Be, Bd and fourth is 2-norm of B
#day declared using datetime module in python
#z1 : indicates we want magnetic field (we can also get the secular variation using 1 instead of 0 here)
#z2 : indicates the height is given in km above sea level
#height : height in km above sea level i.e. altitude
#lat : latitude
#lon : longitude