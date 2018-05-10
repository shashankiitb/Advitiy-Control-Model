import numpy as np
from datetime import *
import constants as cnts
import frames as fs
from pyigrf12 import runigrf12
'''
code takes input:
    position in ecif frame
    time
code gives output:
    magnetic field in ecif frame
'''  
initialtime=datetime(2018, 4, 03, 12, 50, 19) #Enter the starting time in year,month,day,hour,minute,second
equinox=datetime(2018, 3, 20, 13, 05, 00) #Enter the date and time for the closest equinox (Google this up)
sgp_output=np.genfromtxt('sgp_output.csv', delimiter=",")
T = sgp_output[0,:]
N = len(T);
b_output=np.empty([4,N])
delay=0.1 #the time difference between two positions recorded by SGP,
delay=timedelta(seconds=delay) #converted into a format which can be added to datetime 
day = initialtime

'''
def b_calc(x,t):
  z1 = 0
  z2 = 1
  height=np.linalg.norm(x)-cnts.R
  #initdays=initialtime.day+(initialtime.second/86400)
  #day=initdays+(t/86400)  
  v_x_ecef=fs.ecif2ecef(x,t)
  lat,lon=fs.latlon(v_x_ecef)
  B = runigrf12(day,z1,z2,height,lat,lon)
  v_b_ned=np.array([B[0],B[1],B[2]])
  v_b_ecef=fs.ned2ecef(v_b_ned)
  v_b_ecif=fs.ecef2ecif(v_b_ecef)
  v_b_o_est=fs.ecif2orbit(v_b_ecif)
  day = day + delay
  return v_b_ecif
  #B : in nano tesla in NED frame. first 3 components are Bn, Be, Bd and fourth is 2-norm of B
  #day declared using datetime module in python
  #z1 : indicates we want magnetic field (we can also get the secular variation using 1 instead of 0 here)
  #z2 : indicates the height is given in km above sea level
  #height : height in km above sea level i.e. altitude
  #lat : latitude
  #lon : longitude
'''

for i in range (N):
  b_output[0,i]=T[i]
  x=np.array([sgp_output[1,i],sgp_output[2,i],sgp_output[3,i]])
  t = T[i]
  z1 = 0
  z2 = 1
  height=np.linalg.norm(x)-cnts.R
  v_x_ecef=fs.ecif2ecef(x,t)
  lat,lon=fs.latlon(v_x_ecef)
  B = runigrf12(day,z1,z2,height,lat,lon)
  
  v_b_ned=np.hstack((B[0],B[1],B[2]))
  
  v_b_ecef=fs.ned2ecef(v_b_ned,lat,lon)
  DCM = fs.ecif2ecefR(initialtime,equinox,t)
  v_b_ecif=np.dot(np.transpose(DCM),v_b_ecef)
  #v_b_o=fs.ecif2orbit(v_b_ecif)
  day = day + delay

  b_output[1:4,i] = v_b_ecif

np.savetxt("b_output.csv", b_output, delimiter=",")    
    
