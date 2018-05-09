#to understand the names of variable please refer to lightmodel
import numpy as np
from datetime import *
import matplotlib.pyplot as plt
Rearth = 6378164.0 #Radius of Earth in meters
AU = 159597870610.0 #Distance between sun and earth in meters
Rsun = 695500000.0 #Radius of the Sun in meters
sgp_output=np.genfromtxt('sgp_output.csv', delimiter=",")
si_output=np.genfromtxt('si_output.csv', delimiter=",")
T = sgp_output[0,:] #storing first element as time, gives a row vector
positionvectorarray = sgp_output[1:4,:]  #Storing the position vector of satellite given by sgp4 model
N = len(T)
light_output =np.empty([2,N])
Dumbra = AU*Rearth / (Rsun - Rearth) #distance from centre of the earth to the vertex of the umbra cone
Dpenumbra = AU*Rearth / (Rsun + Rearth) #distance from centre of the earth to the vertex of the penumbra cone
alpha = np.arcsin(Rearth / Dumbra) #Half the aperture of the cone made by umbra
beta = np.arcsin(Rearth / Dpenumbra) #Half the aperture of the cone made by penumbra
print
for i in range(N):
    position_satellite = positionvectorarray[:,i] 
    sunvector = si_output[1:4,i]
    #angle between sun light vector and satellite position vector in ECI frame
    angle_sat = np.arccos(np.dot(position_satellite, sunvector) /np.linalg.norm(position_satellite) )
    #angle between the vector from the vertex of the umbra cone to satellite and sun vector
    parameter_umbra = np.arccos((np.dot((position_satellite + Dumbra*sunvector), sunvector)) / np.linalg.norm(position_satellite + Dumbra*sunvector))
    #angle between the vector from the vertex of the peumbra cone to satellite and negative sun vector
    parameter_penumbra =np.arccos((np.dot((position_satellite - Dpenumbra*sunvector), -sunvector)) / np.linalg.norm(position_satellite - Dpenumbra*sunvector))
    #Boolean to store whether satellite is in light or dark. 1 implies satellite is in light.
    if (angle_sat >= np.pi/2 + alpha) & (parameter_umbra <= alpha):
        flag = 0
    elif (angle_sat >=np.pi/2 - beta) & (parameter_umbra > alpha) & (parameter_penumbra <= beta):
        flag = 0.5
    else:
    	flag=1
    light_output[0,i] = T[i]
    light_output[1,i] = flag
np.savetxt("light_output.csv", light_output, delimiter=',')