from solver import rk4Quaternion
import numpy as np
import frames
import unittest
import satellite
from dynamics import x_dot_BO
from constants_1U import G, M_EARTH

def f_constant(sat,t,x):
	return 1.0

def f_ramp(sat,t,x):
	return t

def f_tx(sat,t,x):
	return -t*x
class TestSolver(unittest.TestCase):
	'''
	def test_constant(self):
		t0 = 0.0
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4Quaternion(mySat,f_constant,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)

		self.assertTrue(np.allclose([11.0,10.0,10.0,10.0,10.0,10.0,10.0],mySat.getState()))
	
	def test_ramp1(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4Quaternion(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		
		self.assertTrue(np.allclose([51.0,50.0,50.0,50.0,50.0,50.0,50.0],mySat.getState()))
	
	def test_ramp2(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3]),t0)
		t = 10.
		h = 0.1
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		for i in range(0,int(t/h)):
			x1 = rk4Quaternion(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)                          
		
		self.assertTrue(np.allclose([50.5,50.5,49.5,49.5,51.6,47.5,50.3],mySat.getState()))

	def test_tx(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3]),t0)
		t = 3.
		h = 0.001
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		for i in range(0,int(t/h)):
			x1 = rk4Quaternion(mySat,f_tx,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		
		expected = np.exp(-t**2/2.)*np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3])
		
		self.assertTrue(np.allclose(expected,mySat.getState()))
	'''

	def test_dynamics(self):
		t0 = 0.
		h = 0.001
		
		v_q_BO = np.array([0.4,0.254,-0.508,0.71931912])
		v_q_BI = frames.qBO2qBI(v_q_BO,np.array([1e6,53e5,0.]),np.array([5.60,-5.0,0.0]))
		mySat = satellite.Satellite(np.hstack((v_q_BI, np.array([0.1,-0.05,-0.3]))),t0)
		
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([10e-10,-4e-6,-3e-5]))
		mySat.setControl_b(np.array([1e-5,1e-5,-8e-4]))
		
		r=np.linalg.norm(mySat.getPos())
		v_w_IO_o = np.array([0., np.sqrt(G*M_EARTH/(r)**3), 0.]) #angular velocity of orbit frame wrt inertial frame in orbit frame
		
		v_w_BO_b = frames.wBIb2wBOb(np.array([0.1,-0.05,-0.3]),v_q_BO,v_w_IO_o)
		
		x1 = rk4Quaternion(mySat,x_dot_BO,h)
		mySat.setState(x1.copy())
		mySat.setTime(t0+h)
		
		k1 = h*x_dot_BO(mySat, t0+0.5*h, np.hstack((v_q_BO,v_w_BO_b)))
		k2 = h*x_dot_BO(mySat, t0+0.5*h, np.hstack((v_q_BO,v_w_BO_b))+0.5*k1)
		k3 = h*x_dot_BO(mySat, t0+0.5*h, np.hstack((v_q_BO,v_w_BO_b))+0.5*k2)
		k4 = h*x_dot_BO(mySat, t0+h, np.hstack((v_q_BO,v_w_BO_b))+k3)
		
		error_state = np.hstack((v_q_BO,v_w_BO_b)) + (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)
		expected = np.hstack((frames.qBO2qBI(error_state[0:4],np.array([1e6,53e5,0.]),np.array([5.60,-5.0,0.0])),frames.wBOb2wBIb(error_state[4:7],error_state[0:4],v_w_IO_o)))
		self.assertTrue(np.allclose(expected,mySat.getState()))

if __name__=="__main__":
	unittest.main(verbosity=2)