import numpy as np

def rk42(x0,h,F,T):
#range kutta order 4 solver, assuming magnetic field does not change in time t to t+h
	k1 = h*d2.dynamics2(x0,F,T)
	k2 = h*d2.dynamics2(x0+k1/2,F,T)
	k3 = h*d2.dynamics2(x0+k2/2,F,T)
	k4 = h*d2.dynamics2(x0+k3,F,T)
	x1 = x0.copy()
	#print k3
	x1 = x1 + (k1 + 2*k2 + 2*k3 + k4)/6

	x1[6:10] = x1[6:10]/np.linalg.norm(x1[6:10])
	return x1
