import numpy as np
import disturbance_1U as dist
import unittest
from satellite import Satellite
from constants_1U import m_INERTIA
from ddt import data, ddt , unpack

@ddt
class TestGravityGradient(unittest.TestCase):
	#Test the data type of output
	def test_gg_data_type(self):
		sat = Satellite(np.array([1.,0.,0.,0.,0.,0.,0.]),13.)
		sat.setPos(np.array([7070e3,0.,0.]))
		result = dist.gg_torque(sat)
		self.assertEqual(type(result),np.ndarray)
	
	#Take position vector to be eigen vector of m_INERTIA along with q =[1,0,0,0] thus torque will be zero
	l, w = np.linalg.eig(m_INERTIA)
	@data(7070e3*w[:,0],7070e3*w[:,1],7070e3*w[:,2])
	def test_inertia_eigenvec(self,value):
		state = np.array([1.,0.,0.,0.,0.1,-0.02,-0.2])
		mySat = Satellite(state,128.05)
		mySat.setPos(value)
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		result = dist.gg_torque(mySat)

		self.assertTrue(np.allclose(result,[0.,0.,0.]))

class TestAeroDrag(unittest.TestCase):
	#test the data type of the output
	'''
	def test_aero_data_type(self):
		sat = Satellite(np.array([1.,0.,0.,0.,0.,0.,0.]),13.)
		sat.setPos(np.array([7070e3,0.,0.]))
		sat.setVel(np.array([6.93e3,-2.0,0.]))
		result = dist.aero_torque(sat)
		self.assertEqual(type(result),np.ndarray)
	'''
	def test_aero(self):
		sat = Satellite(np.array([np.sqrt(0.5),-np.sqrt(0.5),0.,0.,0.1,0.23,0.]),13.)
		sat.setPos(np.array([0.,0.,7e6]))
		sat.setVel(np.array([0,2e3,6e3]))
		result = dist.aero_torque(sat)
		print result
		
if __name__=="__main__":
	unittest.main(verbosity=2)