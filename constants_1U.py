#Constants used in the code for simulation of 1U satellite

import numpy as np

W_EARTH = 7.2921150e-5; # rotation velocity of the earth (rad per second)
G = 6.67408e-11; #universal gravitational constant, SI
M = 5.972e24; #mass of earth, kg
R = 6371.0e3; #radius of earth, m

#-- Moment of inertia matrix in kgm^2 for 1U satellite (assumed to be uniform with small off-diagonal)
Ixx = 0.0015
Iyy = 0.0015
Izz = 0.0011
Ixy = -6.39e-6
Iyz = -2.16e-5
Ixz = -5.386e-6

m_INERTIA = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz], [Ixz, Iyz, Izz]])
m_INERTIA_inv = np.linalg.inv(m_INERTIA)	#inverse of inertia matrix

v_q0_BO = np.array([1.,0.,0.,0.])	#unit quaternion initial condition
v_w0_BOB = np.array([0.,-1*math.sqrt(G*M/R**3),0.])	#initial angular velocity
v_STATE0 = np.hstack((q0,w0))	#Initial state vector [q_BO , w_BOB]


CONTROL_STEP = 2.0	#control cycle time period in second
FREQ = 1e3 	#frequency of duty cycle in Hz

INDUCTANCE = 1e-3	#Inductance of torquer
RESISTANCE = 100.0	#Resistance of torquer

v_Ax = np.array([0.01,0.,0.])	#area vector perpendicular to x-axis in m^2
v_Ay = np.array([0.,0.01,0.])	#area vector perpendicular to y-axis in m^2
v_Az = np.array([0.,0.,0.01])	#area vector perpendicular to z-axis in m^2