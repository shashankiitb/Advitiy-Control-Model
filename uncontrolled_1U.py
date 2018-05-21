import numpy as np
import satellite
import disturbance_1U as dist
from constants_1U import v_q0_BO,v_w0_BIB, R_EARTH, ALTITUDE
from dynamics import x_dot
import frames as fs
import solver as sol
import scipy.io as sio
import os
import matplotlib.pyplot as plt
import qnv as qnv
import math

#Read position, velocity, sun-vector in ECIF from data file
#sgp_output = 1e3*np.genfromtxt('sgp_output.csv', delimiter=",")

sgp_output = sio.loadmat('SGP_120k.mat')['SGP_120k'].transpose()

si_output = np.genfromtxt('si_output.csv',delimiter=",")
light_output = np.genfromtxt('light_output.csv',delimiter=",")
init,end = 0,0
for k in range(0,len(light_output)):
	#obtain index corresponding to the start of eclipse
	l1 = light_output[k]
	l2 = light_output[k+1]
	if l1 ==1 and l2 == 0 and count == 0:	#start of eclipse
		init = k
		count = 1
	elif l1==1 and l2==0 and count == 1:	#start of second eclipse
		end = k 
		break
#sgp_output = np.zeros((len(si_output[:,0]),7))
#sgp_output[:,0] = si_output[:,0].copy()
#w = 0.00106178
#sgp_output[:,1] = (R_EARTH+ALTITUDE)*np.cos(w*sgp_output[:,0])
#sgp_output[:,3] = (R_EARTH+ALTITUDE)*np.sin(w*sgp_output[:,0])
#sgp_output[:,4] = -7.5e3*np.sin(w*sgp_output[:,0])
#sgp_output[:,6] = 7.5e3*np.cos(w*sgp_output[:,0])

#define simulation parameters
t0 = sgp_output[init,0]
tf = sgp_output[end,0]	#simulation time in seconds
dt = 0.1	#step size of simulation in seconds
h = 0.1		#step size of integration in seconds
N = int((tf-t0)/dt)+1



print N

#initialize empty matrices
v_state = np.zeros((N,7))
v_q_BO = np.zeros((N,4))
v_w_BOB = np.zeros((N,3))
euler = np.zeros((N,3))
torque_dist = np.zeros((N,3))

v_q0_BI = fs.qBO_2_qBI(v_q0_BO,sgp_output[0,1:4],sgp_output[0,4:7])	
v_state[0,:] = np.hstack((v_q0_BI,v_w0_BIB))
v_q_BO[0,:] = v_q0_BO
v_w_BOB[0,:] = fs.wBIB_2_wBOB(v_w0_BIB,v_q_BO[0,:])
euler[0,:] = qnv.quat2euler(v_q_BO[0,:])

#Make satellite object
Advitiy = satellite.Satellite(v_state[0,:],t0)
Advitiy.setControl_b(np.array([0.,0.,0.]))	#uncontrolled satellite

#-------------Main for loop---------------------
for  i in range(0,N-1):
	if math.fmod(i,N/100) == 0 and i>5:
		print 100*i/N , np.linalg.norm(v_torque_gg_b), np.linalg.norm(v_torque_aero_b), np.linalg.norm(v_torque_solar_b)
		#print v_torque_total_b
	#Set satellite parameters
	if i < int(N/2):
		Advitiy.setLight(0)
	else:
		Advitiy.setLight(1)
	Advitiy.setState(v_state[i,:])
	Advitiy.setTime(t0 + i*dt)
	Advitiy.setPos(sgp_output[i,1:4])
	Advitiy.setVel(sgp_output[i,4:7])
	Advitiy.setSun_i(si_output[i,1:4])
	#calculate the disturbance torques
	v_torque_gg_b = dist.gg_torque(Advitiy).copy()
	v_torque_aero_b = dist.aero_torque(Advitiy).copy()
	v_torque_solar_b = dist.solar_torque(Advitiy).copy()
	
	v_torque_total_b =(v_torque_gg_b + v_torque_aero_b + v_torque_solar_b)
	Advitiy.setDisturbance_b(v_torque_total_b)
	torque_dist[i,:] = v_torque_total_b.copy()

	v_state_next = np.zeros((1,7))

	#Use rk4 solver to calculate the state for next step
	for j in range(0,int(dt/h)):		
		v_state_next = sol.rk4(Advitiy,x_dot,h)
		Advitiy.setState(v_state_next.copy())
		Advitiy.setTime(t0 + i*dt + (j+1)*h)

	v_state[i+1,:] = v_state_next.copy()
	
	#Calculate observable quantities
	
	v_q_BO[i+1,:] = fs.qBI_2_qBO(v_state_next[0:4],Advitiy.getPos(),Advitiy.getVel())
	v_w_BOB[i+1,:] = fs.wBIB_2_wBOB(v_state_next[4:7],v_q_BO[i+1,:])
	euler[i+1,:] = qnv.quat2euler(v_q_BO[i+1,:])


#save the data files
os.chdir('Logs/')
os.mkdir('sso-1U-dist')
os.chdir('sso-1U-dist')
np.save('position',sgp_output[init:end+1,1:4])
np.save('velocity',sgp_output[init:end+1,4:7])

np.save('time',sgp_output[init:end+1,0] - t0)
np.save('w_BOB',v_w_BOB)
np.save('q_BO',v_q_BO)
np.save('state',v_state)
np.save('euler',euler)
np.save('disturbance',torque_dist)

print 'sso-1U-dist'