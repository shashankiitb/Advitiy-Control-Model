from solver import rk4
import numpy as np
import unittest
import satellite
import dynamics as dyn

def f_constant(sat,t,x):
	return 1.0

def f_ramp(sat,t,x):
	return t

def f_tx(sat,t,x):
	return -t*x
class TestSolver(unittest.TestCase):
	def testConstant(self):
		t0 = 0.0
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_constant,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)

		self.assertTrue(np.allclose([11.0,10.0,10.0,10.0,10.0,10.0,10.0],mySat.getState()))

	def testRamp1(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		
		self.assertTrue(np.allclose([51.0,50.0,50.0,50.0,50.0,50.0,50.0],mySat.getState()))
	
	def testRamp2(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3]),t0)
		t = 10.
		h = 0.1

		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)                          
		
		self.assertTrue(np.allclose([50.5,50.5,49.5,49.5,51.6,47.5,50.3],mySat.getState()))

	def testTX(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3]),t0)
		t = 3.
		h = 0.001

		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_tx,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		
		expected = np.exp(-t**2/2.)*np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3])
		
		self.assertTrue(np.allclose(expected,mySat.getState()))
		
	def testReal(self):
	    t0 = 1.5
	    state = np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3])
	    mySat = satellite.Satellite(state,t0)
	    mySat.setControl_b(np.array([-7.3,8.1,5.6]))
	    mySat.setDisturbance_i(np.array([2.4,-8.1,-4.3]))
	    mySat.setPos(np.array([-2.4,8.1,-4.3]))
	    mySat.setVel(np.array([2.4,8.1,-4.3]))

	    k1 = 0.2 * dyn.x_dot(mySat, 1.5, state)
	    k2 = 0.2 * dyn.x_dot(mySat, 1.5+0.1, state+k1/2.0)
	    k3 = 0.2 * dyn.x_dot(mySat, 1.5+0.1, state+k2/2.0)
	    k4 = 0.2 * dyn.x_dot(mySat, 1.5+0.2, state+k3)
	    x2 = state + (k1 + 2.0 * k2 + 2.0 * k3 + k4)/6.0
	    x1 = rk4(mySat,dyn.x_dot,0.2)
	    self.assertTrue(np.allclose(x2,x1))
	    
if __name__=="__main__":
	unittest.main(verbosity=2)