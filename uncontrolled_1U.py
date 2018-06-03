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

#Read position, velocity, sun-vector in ECIF from data file. temp variable for entire file
sgp_output_temp = np.genfromtxt('sgp_output.csv', delimiter=",")

si_output_temp = np.genfromtxt('si_output.csv',delimiter=",")
light_output_temp = np.genfromtxt('light_output.csv',delimiter=",")
init,end ,count= 0,0,0
for k in range(0,len(light_output_temp)-1):
	#obtain index corresponding to the start of eclipse
	l1 = light_output_temp[k,1]
	l2 = light_output_temp[k+1,1]
	if l1 ==0.5 and l2 == 1 and count == 0:	#start of eclipse
		init = k
		count = 1
		
	elif l1==0.5 and l2==1 and count == 1:	#start of second eclipse
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
print init,end
t0 = sgp_output_temp[init,0]
tf = sgp_output_temp[end,0]	#simulation time in seconds
dt = 0.1	#step size of simulation in seconds
h = 0.1		#step size of integration in seconds
N = int((tf-t0)/dt)+1

#extract init to end data from temp file
sgp_output = sgp_output_temp[init:(init+N),:].copy()
si_output = si_output_temp[init:(init+N),:].copy()
light_output = light_output_temp[init:(init+N),:].copy()
print N ,'Simulation for ' ,dt*(N-1),'seconds'

#initialize empty matrices
v_state = np.zeros((N,7))
v_q_BO = np.zeros((N,4))
v_w_BOB = np.zeros((N,3))
euler = np.zeros((N,3))
torque_dist = np.zeros((N,3))

v_q0_BI = fs.qBO2qBI(v_q0_BO,sgp_output[0,1:4],sgp_output[0,4:7])	
v_state[0,:] = np.hstack((v_q0_BI,v_w0_BIB))
v_q_BO[0,:] = v_q0_BO
v_w_BOB[0,:] = fs.wBIb2wBOb(v_w0_BIB,v_q_BO[0,:])
euler[0,:] = qnv.quat2euler(v_q_BO[0,:])

#Make satellite object
Advitiy = satellite.Satellite(v_state[0,:],t0)
Advitiy.setControl_b(np.array([0.,0.,0.]))	#uncontrolled satellite

#-------------Main for loop---------------------
for  i in range(0,N-1):
	if math.fmod(i,N/100) == 0 and i>5:
		print 100*i/N 
		
	#Set satellite parameters
	
	Advitiy.setLight(light_output[i,1])
	Advitiy.setState(v_state[i,:])
	Advitiy.setTime(t0 + i*dt)
	Advitiy.setPos(sgp_output[i,1:4])
	Advitiy.setVel(sgp_output[i,4:7])
	Advitiy.setSun_i(si_output[i,1:4])
	#calculate the disturbance torques
	v_torque_gg_b = dist.gg_torque(Advitiy).copy()
	v_torque_aero_b = dist.aero_torque(Advitiy).copy()
	v_torque_solar_b = dist.solar_torque(Advitiy).copy()
	
	v_torque_total_b =0*(v_torque_gg_b + v_torque_aero_b + v_torque_solar_b)
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
	
	v_q_BO[i+1,:] = fs.qBI2qBO(v_state_next[0:4],Advitiy.getPos(),Advitiy.getVel())
	v_w_BOB[i+1,:] = fs.wBIb2wBOb(v_state_next[4:7],v_q_BO[i+1,:])
	euler[i+1,:] = qnv.quat2euler(v_q_BO[i+1,:])


#save the data files
os.chdir('Logs/')
os.mkdir('sso-identity-no-dist')
os.chdir('sso-identity-no-dist')
np.savetxt('position.csv',sgp_output[:,1:4], delimiter=",")
np.savetxt('velocity.csv',sgp_output[:,4:7], delimiter=",")

np.savetxt('time.csv',sgp_output[:,0] - t0, delimiter=",")
np.savetxt('w_BOB.csv',v_w_BOB, delimiter=",")
np.savetxt('q_BO.csv',v_q_BO, delimiter=",")
np.savetxt('state.csv',v_state, delimiter=",")
np.savetxt('euler.csv',euler, delimiter=",")
np.savetxt('disturbance.csv',torque_dist, delimiter=",")

print 'sso-identity-no-dist'