#Constants used in the code for simulation of 1U satellite

import numpy as np
import datetime as dt
from math import sqrt

#--------Earth and environment
W_EARTH = 7.2921150e-5; # rotation velocity of the earth (rad per second)
G = 6.67408e-11; #universal gravitational constant, SI
M_EARTH = 5.972e24; #mass of earth, kg
R_EARTH = 6371.0e3; #radius of earth, m

v_w_IOO = np.array([0., np.sqrt(G*M_EARTH/R_EARTH**3), 0.]) #w of ecif wrt orbit in orbit frame

#------------date format yyyy,mm,dd
LINE1 = ('1 41783U 16059A   18093.17383152  .00000069  00000-0  22905-4 0  9992') #Insert TLE Here
LINE2 = ('2 41783  98.1258 155.9141 0032873 333.2318  26.7186 14.62910114 80995') 

LAUNCHDATE = dt.datetime(2018, 4, 03, 12, 50, 19)	#date of launch t=0
EQUINOX = dt.datetime(2018, 3, 20, 13, 05, 00)	#day of equinox
steprut = 1.002738 #siderial time = stperut * universal time

#-- --------Moment of inertia matrix in kgm^2 for 1U satellite (assumed to be uniform with small off-diagonal)
MASS_SAT = 0.850	#in kg

Ixx = 0.0015
Iyy = 0.0015
Izz = 0.0011
Ixy = -6.39e-6
Iyz = -2.16e-5
Ixz = -5.386e-6

m_INERTIA = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]])
m_INERTIA_inv = np.linalg.inv(m_INERTIA)	#inverse of inertia matrix

#Satellite Dimensions
Lx = 0.10	#in meters
Ly = 0.10	#in meters
Lz = 0.10	#in meters

#Side panel areas
v_Ax = np.array([0.01,0.,0.])	#area vector perpendicular to x-axis in m^2
v_Ay = np.array([0.,0.01,0.])	#area vector perpendicular to y-axis in m^2
v_Az = np.array([0.,0.,0.01])	#area vector perpendicular to z-axis in m^2

#------------Initial conditions
v_q0_BI = np.array([1.,0.,0.,0.])	#unit quaternion initial condition
v_w0_BIB = np.array([0.,-1*sqrt(G*M_EARTH/R_EARTH**3),0.])	#initial angular velocity
v_STATE0 = np.hstack((v_q0_BI,v_w0_BIB))	#Initial state vector [q_BO , w_BOB]


CONTROL_STEP = 2.0	#control cycle time period in second
FREQ = 1e3 	#frequency of duty cycle in Hz

INDUCTANCE = 1e-3	#Inductance of torquer in Henry
RESISTANCE = 100.0	#Resistance of torquer	in Ohm

#Disturbance model constants
SOLAR_PRESSURE = 4.56e-6	#in N/m^2
REFLECTIVITY = 0.2
r_COM = np.array([-0.067e-2,-0.58e-2,-0.067e-2])

AERO_DRAG = 2.2
RHO = 0.218e-12
