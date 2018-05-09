import numpy as np
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import *
line1 = ('1 41783U 16059A   18093.17383152  .00000069  00000-0  22905-4 0  9992') #Insert TLE Here
line2 = ('2 41783  98.1258 155.9141 0032873 333.2318  26.7186 14.62910114 80995') 
satellite = twoline2rv(line1, line2, wgs72) #wgs72 is a particular model used by sgp4
initialtime=datetime(2018, 4, 03, 12, 50, 19) #Enter the starting time in year,month,day,hour,minute,second
delay=0.1 #Enter the delay between each consecutive data points in seconds
totaltime=98.4*60 #Enter the time for which SGP Data should be created from the initial time 
N=int(totaltime/delay) #Number of iterations for which SGP4 module will be called
delay=timedelta(seconds=delay) #Converts the delay into a form that can be added to datetime objects
sgp_output=np.empty([7,N])
time=initialtime
for i in range (N):
	time=time+delay
	sgp_output[0,i]=i*0.1 #Stores the time after initialtime for which positon and velocity is calculated
	sgp_output[1:4,i]=satellite.propagate(time.year,time.month,time.day,time.hour,time.minute,time.second)[0] #Stores the position
	sgp_output[4:7,i]=satellite.propagate(time.year,time.month,time.day,time.hour,time.minute,time.second)[1] #Stores the velocity, Reshape is necessary to match dimensions
np.savetxt("sgp_output.csv", sgp_output, delimiter=",") #Saves sgp_output to csv file