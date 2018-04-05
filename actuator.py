#Function to calculate the current from t=0 to t=tf  
import numpy as np
import math as math
from constants import *


def duty_generate(i_control,R):
    duty=(i_control*R)/3.3
    return duty

def internal_step_for_torquer(duty,freq):
    #dt_h = 0.1*duty/freq 	#step size for high cycle
    #dt_l = 0.01*(1.0-duty)/freq 	#step size for low cycle
    dt_h = np.array([0.1,0.1,0.1])
    dt_l = np.array([0.1,0.1,0.1])
    dt_l=dt_l.min();
    return np.hstack((dt_h,dt_l))

#Inputs: inductance, resistance, final time, frequency, duty cycle(from 0.0 to 1.0) [all floats]
def current_LR_PWM(tf,duty_self,dt,duty_cycle):	#Returns the tuple with [t,i] where t is from 0 to tf.
	L = inductance
	R = resistance

	V_m = 3.3
	T = 1.0/freq
	tau = L/R

	dt = dt[dt.argsort()[::1]]
	#print duty_cycle
	duty_cycle = duty_cycle[duty_cycle.argsort()[::1]]
	
	t0 = 0.0
	t1 = duty_cycle[0]/freq
	t2 = duty_cycle[1]/freq
	t3 = duty_cycle[2]/freq
	#print duty_cycle[1]-duty_cycle[0]
	#print duty_cycle[0]/dt[0], tf*(duty_cycle[1]-duty_cycle[0])/dt[1]
	N = int(tf*duty_cycle[0]/dt[0]) + int(tf*(duty_cycle[1]-duty_cycle[0])/dt[1]) 
	N = N + int(tf*(duty_cycle[2]-duty_cycle[1])/dt[2]) + int(tf*(1.0-duty_cycle[2])/dt[3]) +3
	
	time = np.zeros(N)
	i = np.zeros(N)
	v = np.zeros(N)
	
	i0_h = 0.0	#current at start of high cycle
	i0_l = 0.0	#current at the start of low cycle
	

	t = 0.0
	k = 0 
	t_curr = 0.0
	while (t<=tf):

		 
		if math.fmod(t,T) <= duty_self*T :
			t_curr = math.fmod(t,T)
			i[k] = (V_m/R) + (i0_h - V_m/R)*np.exp(-t_curr/tau)
			v[k] = V_m
			
			i0_l = i[k] 
			
			if math.fmod(t,T) < t1:
				t = t + dt[0]
			elif math.fmod(t,T)>= t1 and math.fmod(t,T)<t2:
				t = t +dt[1]
			elif math.fmod(t,T) >= t2 and math.fmod(t,T)<t3:
				t = t +dt[2]
			else:
				t = t + dt[3]
			
			#t = t +0.1
		else:
			t_curr = math.fmod(t,T) - duty_self*T
			i[k] = i0_l*np.exp(-t_curr/tau)
			
			v[k] = 0.0
			
			i0_h = i[k]
			
			if math.fmod(t,T) < t1:
				t = t + dt[0]
			elif math.fmod(t,T)>= t1 and math.fmod(t,T)<t2:
				t = t +dt[1]
			elif math.fmod(t,T) >= t2 and math.fmod(t,T)<t3:
				t = t +dt[2]
			else:
				t = t + dt[3]
			
			#t = t+0.1
		k = k+1
		time[k] = t
		#print t
	
	return time, i, v

'''

#Test code
#current_LR_PWM(L,R,tf,freq,duty,dt,duty_cycle):
import matplotlib.pyplot as plt
tf = 3.0
freq = 1.0
curr_duty = 0.5

duty_cycle = np.array([0.5,0.5,0.5])
dt = np.zeros(4)
dt[0] = 0.001#*duty_cycle[0]/freq 	#step size for high cycle
dt[1] = 0.001#*duty_cycle[1]/freq
dt[2] = 0.001#*duty_cycle[2]/freq	#step size for low cycle
dt[3] = 0.001#*(1.-0.33)/freq
x = current_LR_PWM(1.,100.0,tf,freq,curr_duty,dt,duty_cycle)


plt.plot(x[0],x[2])
#plt.show()
plt.plot(x[0],x[1])
plt.show()
print dt
print tf*duty_cycle[0]/dt[0], tf*(duty_cycle[1]-duty_cycle[0])/dt[1]
print tf*(duty_cycle[2]-duty_cycle[1])/dt[2], tf*(1.0-duty_cycle[2])/dt[3]
'''