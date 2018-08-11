import numpy as np
import frames
from constants_1U import G, M_EARTH

def rk4Quaternion(sat,f,h): #This is Runge Kutta-4 solver for ordinary differential equation.
	'''
		Input is satellite object, f (derivative of state vector (quaternion and angular velocity)) and integration step size
		It returns value of state at next time (after a time step of h) (x(t+h)) using f and value of state at current time x(t)
	'''
	v_state_exact_0 = sat.getState()	#state at t = t0	
	t = sat.getTime() 
	v_q_BO = frames.qBI2qBO(v_state_exact_0[0:4],sat.getPos(),sat.getVel()) #calculating error quaternion
	r=np.linalg.norm(sat.getPos())
	v_w_IO_o = np.array([0., np.sqrt(G*M_EARTH/(r)**3), 0.]) #angular velocity of orbit frame wrt inertial frame in orbit frame
	v_w_BO_b = frames.wBIb2wBOb(v_state_exact_0[4:7],v_q_BO,v_w_IO_o) #calculating w_BO_b
	print(v_w_BO_b)
	v_state_error_0 = np.hstack((v_q_BO,v_w_BO_b)) #calculating error state

	#rk-4 routine
	k1 = h*f(sat, t, v_state_error_0)
	k2 = h*f(sat, t+0.5*h, v_state_error_0+0.5*k1)
	print(k2)
	k3 = h*f(sat, t+0.5*h, v_state_error_0+0.5*k2)
	k4 = h*f(sat, t+h, v_state_error_0+k3)

	v_state_error_new = v_state_error_0 + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)
	
	#Normalize to obtain unit quaternion (different from regular rk4 solver)	
	v_state_error_new[0:4] = v_state_error_new[0:4].copy()/np.linalg.norm(v_state_error_new[0:4].copy()) #error state at t0+h
	
	v_q_BI = frames.qBO2qBI(v_state_error_new[0:4],sat.getPos(),sat.getVel()) #calculating q_BI
	v_w_BI_b = frames.wBOb2wBIb(v_state_error_new[4:7],v_state_error_new[0:4],v_w_IO_o) #calculating w_BO_b
	v_state_exact_new = np.hstack((v_q_BI,v_w_BI_b)) #state at t0+h

	if v_state_exact_new[0] < 0. :
		v_state_exact_new[0:4] = -v_state_exact_new[0:4].copy()
	
	return v_state_exact_new
