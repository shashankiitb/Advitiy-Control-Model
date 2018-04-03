import numpy as np
import forceTorque as ft
import solver as slv
import math
import qnv
from constants import * 
import scipy.io as sio
import time
import datetime
import os
#simulation variables
dir_now = os.path.normpath(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
t1 = time.time()
time_i = 0
#time_f = math.pi/(2*math.sqrt(G*M/R**3))
time_f = 80000.*2
step_size = 0.1
nT = int((time_f - time_i)/step_size)
state = np.zeros((7,nT+1)) #state = (pos from earth in ECIF, velocity, quaternion, angular velocity wrt ECIF in body frame) quaternion rotates body frame vector into inertial frame and defined as (scalar,vector)
state[:,0] = state0.reshape((1,13))
s_time = time_i #simulation time

for n in range(0,nT):
	if (n%10000==0):
		t2 = time.time()
		t3 = t2 - t1
		print n*step_size
		print t3
		print dot[n]
	
	state_now = state[:,n].reshape((13,1))
	state[:,n+1] = (slv.rk43(state_now, step_size, B, s_time)).reshape((1,13))
	s_time = s_time + step_size
	
	
t2 = time.time()
t3 = t2 - t1
print t3


os.chdir('Logs-With-Torque-2')
os.mkdir(dir_now)
os.chdir(dir_now)
sio.savemat('state.mat', mdict={'state':state})
sio.savemat('r.mat', mdict={'r':r})
sio.savemat('dot.mat', mdict={'dot':dot})
sio.savemat('energy.mat', mdict={'energy':energy})
sio.savemat('omega.mat', mdict={'omega':omega})


