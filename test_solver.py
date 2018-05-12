from solver import rk4
import numpy as np
import unittest
import satellite

def f_constant(sat,t,x):
	return 1.0

def f_ramp(sat,t,x):
	return t

def f_tx(sat,t,x):
	return -t*x
class TestSolver(unittest.TestCase):
	def test_constant(self):
		t0 = 0.0
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_constant,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)

		self.assertTrue(np.allclose([11.0,10.0,10.0,10.0,10.0,10.0,10.0],mySat.getState()))

	def test_ramp1(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),t0)
		t = 10
		h = 0.1
		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)
		
		self.assertTrue(np.allclose([51.0,50.0,50.0,50.0,50.0,50.0,50.0],mySat.getState()))
	
	def test_ramp2(self):
		t0 = 0.
		mySat = satellite.Satellite(np.array([0.5,0.5,-0.5,-0.5,1.6,-2.5,0.3]),t0)
		t = 10.
		h = 0.1

		for i in range(0,int(t/h)):
			x1 = rk4(mySat,f_ramp,h)
			mySat.setState(x1.copy())
			mySat.setTime(t0+(i+1)*h)                          
		
		self.assertTrue(np.allclose([50.5,50.5,49.5,49.5,51.6,47.5,50.3],mySat.getState()))

	def test_tx(self):
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


if __name__=="__main__":
	unittest.main(verbosity=2)