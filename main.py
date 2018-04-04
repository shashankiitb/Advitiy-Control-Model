#import statements
from satellite import Satellite
import numpy as np
import math as math
import controller as ctrl
from PWM_current import *
time_f = 6000.0	#in seconds
time = 0.0
dt_model = 0.1	#step size used in model
nT = int((time_f - time_i)/dt_model)
t1 = time.time() #to keep track of processor time
#Orbit and environment model load

v_pos_i = np.array([0.,0.,0.])
v_vel_i = np.array([0.,0.,0.])
v_mag_i = np.array([0.,0.,0.]) 
v_sv_i = np.array([0.,0.,0.])
light = 0
state = np.zeros((nT+1,7))
#initial conditions attitude rates 
v_q_BO_init = np.array([1.,0.,0.,0.])
v_w_BOB_init = np.array([0.,0.,0.])	#in rad/sec
state_init = np.zeros(7)
state_init[0:3] = v_q_BO_init.copy()
state_init[4:6] = v_w_BOB_init.copy()
current = np.array([0.,0.,0.])
duty_cycle = 0.0

###################
Advitiy = Satellite.(state_init,0.)

for n in range(0,nT): #This is main loop it runs from t=0 to t=time_f
	if (n%10000==0):
		t2 = time.time()
		t3 = t2 - t1
		print n*dt_model
		print t3		
	####------------Extracting data from model
	time = n*dt_model	
	v_pos_i = #read from file 	
	v_vel_i = #read from file	
	v_sv_i = #read from file	
	v_mag_i = #read from file	
	light = #read from file

	##-------Set orbit parameters to satellite
	Advitiy.setTime(time)
	Advitiy.setPos(v_pos_i)
	Advitiy.setVel(v_vel_i)
	Advitiy.setSun_i(v_sv_i)
	Advitiy.setMag_i(v_mag_i)
	Advitiy.setLight(light)
	##------Sensor model
	v_sv_o = Advitiy.getSun_o()
	v_sv_b = quatRotate(Advitiy.getQ,v_sv_o)
	v_sv_b_m = sunsensor(v_sv_b)	#get measured sun vector from sunsensor model @Sumit
	
	v_mag_o = Advitiy.getMag_o()
	v_mag_b = quatRotate(Advitiy.getQ,v_mag_o)
	v_mag_b_m = magmeter(v_mag_b)	#get measured mag vector from magmeter model

	Advitiy.setSun_b_m(v_sv_b_m)
	Advitiy.setMag_b_m(v_mag_b_m)
	####------------QUEST
	v_q_BO_m = quest(Advitiy)
	Advitiy.setQUEST(v_q_BO_m)
	#####-----------Calculate disturbances
	v_torque_dist_i = calculate_disturbance(Advitiy)	#vedant
	Advitiy.setDisturbance_i(v_torque_dist_i)
	##-------------Control law
	if(math.fmod(time,control_step) == 0):
		current = ctrl.controlLaw(Advitiy,control_step)
	duty_cycle = calculate_duty(current)
	dt_h = 0.1	#Ram set time steps
	dt_l = 0.1
	torquer_current = PWM_current(L,R,dt_model,freq,duty_cycle,dt_h,dt_l)

	##---------Loop for 0.1 sec in finer steps
	#update control torque
	#propagate the satellite dynamics
	#store the state


	Advity.setState()	#update state add input as well


t2 = time.time()
t3 = t2 - t1
print t3

#code to store logs
os.chdir('Logs')
os.mkdir(dir_now)
os.chdir(dir_now)
sio.savemat('state.mat', mdict={'state':state})












