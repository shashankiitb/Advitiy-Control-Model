import numpy as np

def rk4(sat,f,h): #This is Runge Kutta-4 solver for ordinary differential equation.
	'''
		Input is satellite object, f (derivative of state vector (quaternion and anguar velocity)) and integration step size
		It returns value of state at next time (after a time steo of h) (x(t+h)) using f and value of state at current time x(t)
	'''
	v_state_0 = sat.getState()	#state at t = t0	
	t = sat.getTime()

	#rk-4 routine
	k1 = h*f(sat, t, v_state_0)
	k2 = h*f(sat, t+0.5*h, v_state_0+0.5*k1)
	k3 = h*f(sat, t+0.5*h, v_state_0+0.5*k2)
	k4 = h*f(sat, t+h, v_state_0+k3)

	v_state_new = v_state_0 + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)

	v_state_new[0:4] = v_state_new[0:4]/np.linalg.norm(v_state_new[0:4]) 
	
	return v_state_new
