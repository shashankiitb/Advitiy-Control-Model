from satellite import Satellite
import numpy as np
import math as math
import controller as ctrl
import datetime
from dynamics import *
from sensor import *
from estimator import *
import time
import qnv
from constants import *
from solver import rk42
from frames import ecif2orbit
import scipy.io as sio
import os
dir_now = os.path.normpath(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
def current_LR_PWM(L,R,tf,freq,duty,dt):	#Returns the tuple with [t,i] where t is from 0 to tf.
	#dt = 0.001*duty/freq
	V_m =3.3
	if duty < 0.0:
		flag = -3.3
	else:
		flag = 3.3
	duty = abs(duty)
	print duty
	#N = int(duty*tf/dt_h)+int((1.-duty)*tf/dt_l) + 2
	N = int(tf/dt)+2
	#print N
	time = np.zeros(N)
	i = np.zeros(N)
	v = np.zeros(N)
	T = 1.0/freq
	tau = L/R
	i0_h = 0.0	#current at start of high cycle
	i0_l = 0.0	#current at the start of low cycle
	t = 0.0
	k = 0 
	t_curr = 0.0
	while (t<=tf):

		 
		if math.fmod(t,T) < duty*T :
			t_curr = math.fmod(t,T)
			i[k] = (V_m/R) + (i0_h - V_m/R)*np.exp(-t_curr/tau)
			v[k] = V_m
			i0_l = i[k]
			t = t + dt
			print V_m/R
		else:
			t_curr = math.fmod(t,T) - duty*T
			i[k] = i0_l*np.exp(-t_curr/tau)
			v[k] = 0.0
			i0_h = i[k]
			t = t + dt
			
		k = k+1
		time[k] = t
		#print t
	#print k
	return time, flag*i, v


def dynamics(state,torque):
	Ixx =  .17007470856
	Iyy =  .17159934710
	Izz =  .15858572070
	Ixy = -.00071033134
	Iyz = -.00240388659
	Ixz = -.00059844292
	J = np.array([[Ixx, Ixy, Ixz], [Ixy, Iyy, Iyz],[Ixz, Iyz, Izz]])
	#J = np.identity(3)
	R_e = 6378164 + 817000   
	mu=6.673e-11*5.9742e24   
	s_W_SAT =math.sqrt(mu/(R_e**3))  
	wd = np.array([0,-s_W_SAT,0])
	dw = state[4:7]
	s = state[0:4]
	s0 = s[0]
	sv = s[1:4]
	
	Rs = qnv.quat2rotm(s)
	w = dw + np.dot(Rs,wd)

	s_dot1 = -0.5*np.dot(sv,dw)
	s_dot2 = 0.5*(s0*dw + np.cross(sv,dw))
	s_dot = np.hstack((s_dot1,s_dot2))

	dw_dot = -np.cross(w,np.dot(J,w)) + torque -np.dot(J,np.dot(Rs,np.cross(dw,wd)))

	return np.hstack((s_dot,dw_dot))


def rk42(x0,h,F):
#range kutta order 4 solver, assuming magnetic field does not change in time t to t+h
	k1 = h*dynamics(x0,F)
	k2 = h*dynamics(x0+k1/2,F)
	k3 = h*dynamics(x0+k2/2,F)
	k4 = h*dynamics(x0+k3,F)
	x1 = x0.copy()
	#print k3
	x1 = x1 + (k1 + 2*k2 + 2*k3 + k4)/6

	x1[0:4] = x1[0:4]/np.linalg.norm(x1[0:4])
	return x1

time_f = 10.0	#in seconds
time_now = 0.0
time_i = 0.0
dt_model = 0.1	#step size used in model
nT = int((time_f - time_i)/dt_model)
step = 1e-3
sgp_output=np.genfromtxt('sgp_output.csv', delimiter=",")
si_output=np.genfromtxt('si_output.csv', delimiter=",")
light_output=np.genfromtxt('light_output.csv',delimiter=",")
b_output=np.genfromtxt('b_output.csv',delimiter=",")

state = np.zeros((nT+1,7))
state_dc = np.zeros((nT+1,7))
state[0,:] = np.array([1.0,0.0,0.0,0.0,0.1,0.21,0.53])
state_dc[0,:] = state[0,:].copy()
L_torquer = 1.42e-3
R_torquer = 140.0
frequency = 61.
Kd = 1e-5
N = 60.
A = 0.09
VMAX = 3.3
for n in range(0,nT):

	v_state_now = state[n,:].copy()
	v_state_now_dc = state_dc[n,:].copy()
	#print v_state_now[6]
	#obtain position
	v_pos_now = sgp_output[1:4,n]
	v_vel_now = sgp_output[4:7,n]
	#obtain magnetic field in ECIF in nT
	v_B_now = b_output[1:4,n]*1e-9
	v_B_o = ecif2orbit(v_pos_now,v_vel_now,v_B_now)
	v_B_b = qnv.quatRotate(v_state_now[0:4],v_B_o)
	#obtain torque desired
	#v_dtorque = -k1*state_now[3:6]
	#obtain magnetic moment required
	#v_m = Kd*v_state_now[4:7]/(np.linalg.norm(v_B_now))**2
	v_m = np.array([6,1,-2])
	#obtain current required
	v_i = v_m/(N*A)
	#obtain voltage required
	v_V = v_i/R_torquer
	#print v_V
	if v_V[0] > VMAX:
		v_V[0] = VMAX
		print "toohigh"
	if v_V[1] >VMAX:
		v_V[1] = VMAX
		print "toohigh"
	if v_V[2] > VMAX:
		v_V[2] =VMAX
		print "toohigh"
	v_duty = v_V/VMAX
	#print v_duty
	#obtain current response of LR circuit
	t_LR_x = current_LR_PWM(L_torquer,R_torquer,dt_model,frequency,v_duty[0],step)
	t_LR_y = current_LR_PWM(L_torquer,R_torquer,dt_model,frequency,v_duty[1],step)
	t_LR_z = current_LR_PWM(L_torquer,R_torquer,dt_model,frequency,v_duty[2],step)
	#print type(t_LR_x[1])
	v_i_LR = np.array([t_LR_x[1],t_LR_y[1],t_LR_z[1]]).transpose()
	#print v_i_LR
	v_t_LR = t_LR_x[0]
	v_state_now_f = v_state_now.copy()
	#print v_duty
	for i in range(0,v_t_LR.shape[0]-1):
		#print 'fine state',v_state_now_f
		h = v_t_LR[i+1]-v_t_LR[i]
		torque = N*A*np.cross(v_i_LR[i,:],v_B_now)

		#torque_dc = N*A*np.cross(v_i,v_B_now)
		v_state_next_f = rk42(v_state_now_f,h,torque)
		v_state_now_f = v_state_next_f.copy()
	#simulate dynamics
	#simulate dc dynamics
	v_state_next_dc = rk42(v_state_now_dc,0.1,N*A*np.cross(v_i,v_B_now))
	state[n+1,:] = v_state_now_f.copy()
	state_dc[n+1,:] = v_state_next_dc
pwm = t_LR_x[2]
os.chdir('Logs')
#os.mkdir(dir_now)
#os.chdir(dir_now)
sio.savemat('state.mat', mdict={'state':state})
sio.savemat('state_dc.mat',mdict={'state_dc':state_dc})
sio.savemat('pwm.mat',mdict={'pwm':pwm})


