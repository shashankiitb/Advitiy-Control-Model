#import statements
from satellite import Satellite
import numpy as np
import math as math
import controller as ctrl
from actuator import *
from dynamics import *
from sensor import *
from estimator import *
import time
from qnv import quatRotate
from constants import *

time_f = 10.0	#in seconds
time_now = 0.0
time_i = 0.0
dt_model = 0.1	#step size used in model
nT = int((time_f - time_i)/dt_model)
t1 = time.time() #to keep track of processor time
#Orbit and environment model load

sgp_output=np.genfromtxt('sgp_output.csv', delimiter=",")
si_output=np.genfromtxt('si_output.csv', delimiter=",")
light_output=np.genfromtxt('light_output.csv',delimiter=",")
#mag_output=np.genfromtxt('mag_output.csv',delimiter=",")
state = np.zeros((nT+1,7))
#initial conditions attitude rates 
v_q_BO_init = np.array([1.,0.,0.,0.])
v_w_BOB_init = np.array([0.001,0.,0.])	#in rad/sec
state_init = np.zeros(7)
state_init[0:4] = v_q_BO_init.copy()
state_init[4:7] = v_w_BOB_init.copy()
#print "state-nit" , state_init
current = np.array([0.,0.,0.])
duty_cycle = 0.0

###################
Advitiy = Satellite(state_init,0.)

for n in range(0,nT): #This is main loop it runs from t=0 to t=time_f
	if (n%2==0):
		t2 = time.time()
		t3 = t2 - t1
		print "current index = ",n*dt_model, "current time = ", t3
		print t3		
	##------------Extracting data from model
		
	time_now = n*dt_model	
	v_pos_i = np.array(sgp_output[1:4,n])	#read from file 	
	v_vel_i = np.array(sgp_output[4:7,n])	#read from file	
	v_sv_i = np.array(si_output[1:4,n])	#read from file		
	v_mag_i = np.array([1.,1.,1.])
	light = np.array(light_output[1,n]) #read from file

	#print "state",Advitiy.getState()
	##-------Set orbit parameters to satellite
	
	Advitiy.setPos(v_pos_i)
	Advitiy.setVel(v_vel_i)
	Advitiy.setSun_i(v_sv_i)
	Advitiy.setMag_i(v_mag_i)
	Advitiy.setLight(light)	#!!!
	##------Sensor model
	v_sv_o = Advitiy.getSun_o()

	v_sv_b = quatRotate(Advitiy.getQ(),v_sv_o)
	v_sv_b_m = sunsensor(v_sv_b)	#get measured sun vector from sunsensor model @Sumit
	
	v_mag_o = Advitiy.getMag_o()
	v_mag_b = quatRotate(Advitiy.getQ(),v_mag_o)
	v_mag_b_m = magmeter(v_mag_b)	#get measured mag vector from magmeter model

	v_w_bob = np.array([0.001,0.,0.])
	v_w_bob_m = gyro(v_w_bob)
	Advitiy.setOmega_m(v_w_bob_m)


	Advitiy.setSun_b_m(v_sv_b_m)
	Advitiy.setMag_b_m(v_mag_b_m)
	##------------QUEST
	v_q_BO_m = quest(Advitiy)
	Advitiy.setQUEST(v_q_BO_m)
	##-----------Calculate disturbances
	v_torque_dist_i = calculate_disturbance(Advitiy)	#vedant!!
	Advitiy.setDisturbance_i(v_torque_dist_i)
	##-------------Control law
	if(math.fmod(time_now,control_step) == 0):
		current = ctrl.controlLaw(Advitiy,control_step)
		
	duty_cycle = duty_generate(current,R)
	dt = internal_step_for_torquer(duty_cycle,freq)
	#print time_now,current
	torquer_current_x = current_LR_PWM(dt_model,duty_cycle[0],dt,duty_cycle)[1]
	torquer_current_y = current_LR_PWM(dt_model,duty_cycle[0],dt,duty_cycle)[1]
	torquer_current_z = current_LR_PWM(dt_model,duty_cycle[0],dt,duty_cycle)[1]
	time_fine_loop = current_LR_PWM(dt_model,duty_cycle[0],dt,duty_cycle)[0]
	N_fine = time_fine_loop.shape[0]
	state_fine = np.zeros((N_fine,7))
	state_fine[0,:] = Advitiy.getState()
	state_now = state_fine[0,:]
	##---------Loop for 0.1 sec in finer steps
	#update control torque
	#propagate the satellite dynamics
	#store the state
	#print type(torquer_current_z[0])
	#print 'fine iterations = ',N_fine
	for i in range(0,N_fine-1):

		dt_fine = time_fine_loop[i+1]-time_fine_loop[i]
		curr_now = np.array([torquer_current_x[i],torquer_current_y[i],torquer_current_z[i]])
		v_torque_control_b = control_torque(curr_now,v_mag_b)
		#print v_torque_control_b
		#state_now = state_fine[i,:].copy()
		#print "state_now_1",state_now
		state_new = rk4_x(x_dot,state_now,dt_fine,v_torque_control_b,Advitiy.getDisturbance_b())
		state_now = state_new.copy()
		state_fine[i+1,:] = state_now.copy()
		#print "state_now",state_now
	
	Advitiy.setState(state_now)	#update state add input as well
	state[n,:] = Advitiy.getState()
	Advitiy.setTime(time_now)
t2 = time.time()
t3 = t2 - t1
print t3

#code to store logs
#os.chdir('Logs')
#os.mkdir(dir_now)
#os.chdir(dir_now)
#sio.savemat('state.mat', mdict={'state':state})












