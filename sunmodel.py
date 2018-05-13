import numpy as np
from datetime import *
from constants_1U import LAUNCHDATE, EQUINOX


sgp_output=np.genfromtxt('sgp_output.csv', delimiter=",")
#initialtime = datetime(2018, 4, 03, 12, 50, 19) #Enter the starting time in year,month,day,hour,minute,second
#equinox = datetime(2018, 3, 20, 13, 05, 00) #Enter the date and time for the closest equinox (Google this up)
T = sgp_output[:,0]

N = len(T)
si_output = np.zeros((N,4))

initialdelay = (LAUNCHDATE - EQUINOX).days + (LAUNCHDATE - EQUINOX).seconds/86400.0 #Initial Delay in days


for i in range (N):
	time = initialdelay + T[i] / 86400. #The time passed from equinox till each point in orbit in days
	theta = (2*np.pi*time) / 365.256363 #Angle between intermediate frame (s) and (epsilon) frame about common z-axis
	epsilon = 23.5 * np.pi / 180. #Angle between rotation axis and orbital plane normal
	x=np.cos(theta)#components as got from document reffered
	y=np.sin(theta)*np.cos(epsilon) 
	z=np.sin(theta)*np.sin(epsilon) 
	v_Sun = [x, y, z] #sun vector in ECI Frame
	si_output[i,0] = T[i] #first component is time
	si_output[i,1:4] = v_Sun;
print np.shape(si_output)
np.savetxt("si_output.csv", si_output, delimiter=",") #Saves sgp_output to csv file
