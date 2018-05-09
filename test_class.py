import numpy as np
import math
from cmath import *
from dynamics import * 
from satellite import Satellite
from actuator import *

#from satellite import Satellite
'''
class Satellite:

	def __init__(self,state0,time0):

		self.time = time0
		self.setState(state0)		
		print "init"
	def setState(self,state):

		self.state = state.copy()


sat = Satellite(np.array([1,2]),30.0)

#sat.display()

state = np.array([1.,0.,0.,0.,2.,3.,4.])
advitiy = Satellite(state,1)
a = 2
b = a
#c = a.copy()
#b[0] = 10
print a,b
b = 10
print b,a

tf = 1.0
freq = 10.0
curr_duty = 0.03

duty_cycle = np.array([0.01,0.02,0.03])
dt = np.zeros(4)
dt[0] = 0.01*duty_cycle[0]/freq 	#step size for high cycle
dt[1] = 0.01*duty_cycle[1]/freq
dt[2] = 0.01*duty_cycle[2]/freq	#step size for low cycle
dt[3] = 0.01*(1-0.03)/freq

print tf*duty_cycle[0]/dt[0], tf*(duty_cycle[1]-duty_cycle[0])/dt[1]
print tf*(duty_cycle[2]-duty_cycle[1])/dt[2], tf*(1.0-duty_cycle[2])/dt[3]



def order(x):
	n = 0.0
	while (x<1.):
		x = x*10.
		n = n-1.
	return 10**n

y = np.array([[20.,8.,1.],[5.,6.,9.]])

print np.amin(y,axis=1)

'''

#current_LR_PWM(tf,duty_vec,dt,duty_cycle):

tf = 2.0
my_duty = np.array([[0.2,0.3,0.5],[1.,-1.,1.]])
dt = np.array([0.1,0.1,0.1,0.1])
x = current_LR_PWM(tf,my_duty[:,1],dt,my_duty[0,:])
#print x[1]