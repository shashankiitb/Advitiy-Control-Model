import numpy as np
import math
from constants import * 
import scipy.io as sio
import time
import datetime
import os

dir_now = os.path.normpath(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')) #for storing log files
t1 = time.time() #to keep track of processor time
time_i = 0 #time at which simulation starts
time_f = 80000.*2 #time till which simulation needs to be executed in seconds
step_size = 0.1 #simulation step size in seconds
nT = int((time_f - time_i)/step_size) #number of steps in the simulation
state = np.zeros((nT+1,7)) #state = (quaternion, angular velocity wrt ECIF in body frame) quaternion rotates body frame vector into inertial frame and defined as (scalar,vector)
state[0,:] = v_STATE0
s_time = time_i #simulation time
day = dt.datetime(2017,5,30) #year, month, day

#begin main loop
for n in range(0,nT):
	if (n%10000==0):
		t2 = time.time()
		t3 = t2 - t1
		print n*step_size
		print t3
		
	
	state_now = state[:,n]
	
	#add estimator, controller, environment model, actuator and rigid body dynamics here


	#update satellite parameters using SGP, Bi, Si, Light files here

	s_time = s_time + step_size

	#add code to increment day by step_size
	
	
t2 = time.time()
t3 = t2 - t1
print t3

#code to store logs
os.chdir('Logs')
os.mkdir(dir_now)
os.chdir(dir_now)
sio.savemat('state.mat', mdict={'state':state})

'''
'''
