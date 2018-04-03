import numpy as np
import datetime as dt
import math
import qnv
w_earth = 7.2921159e-5; #rad per second
G=6.67e-11; #universal gravitational constant, SI
M=5.972e24; #mass of earth, kg
R=6371.8e3; #radius of earth, m


Ixx = .17007470856
Iyy = .17159934710
Izz = .15858572070
Ixy = .00071033134
Iyz = .00240388659
Ixz = .00059844292

m_INERTIA = np.array([[Ixx, -1*Ixy, -1*Ixz], [-1*Ixy, Iyy, -1*Iyz], [-1*Ixz, -1*Iyz, Izz]])
m_INERTIA_inv = np.linalg.inv(m_Inertia)

#m_eu98 = np.array([[0.,0.,-1.], [math.cos(incl),math.sin(incl),0.], [math.sin(incl),-math.cos(incl),0.]])
#m_eu0 = np.array([[0.,0.,-1.],[1.,0.,0.],[0,-1.,0.]])
q0 = np.array([1,0,0,0])
w0 = np.array([0.,-1*math.sqrt(G*M/dist0**3),0.]) 
#w0 = np.array([[0.], [0.], [0.]])
v_STATE0 = np.hstack((q0,w0))







