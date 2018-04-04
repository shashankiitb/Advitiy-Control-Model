import numpy as np
import math
from satellite import Satellite
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
'''
state = np.array([1.,0.,0.,0.,2.,3.,4.])
advitiy = Satellite(state,1)
a = 2
b = a
#c = a.copy()
#b[0] = 10
print a,b
b = 10
print b,a