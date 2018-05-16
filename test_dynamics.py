import numpy as np
import unittest
import satellite
from dynamics import x_dot 
from constants_1U import m_INERTIA
from ddt import ddt, data, unpack

@ddt
class TestDynamics(unittest.TestCase):
	def test_zero_torque_rates_ideal_q(self):	#zero torque, zero initial angular velocity, aligned frames
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),12.0)
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot(mySat,12.0,mySat.getState())
		self.assertTrue(np.allclose(result,[0.,0.,0.,0.,0.,0.,0.]))

	def test_zero_torque_ideal_q(self):
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,-0.1,0.39,-0.7]),12.05)
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot(mySat,12.06,mySat.getState())
		self.assertTrue(np.allclose(2.*result[0:4],[0.,-0.1,0.39,-0.7]))
	
	l, w = np.linalg.eig(m_INERTIA)

	#@data(w[:,0].conj(),w[:,1].conj(),w[:,2].conj())
	@data(w[:,0],w[:,1],w[:,2])
	def test_inertia_eigenvec(self,value):
		q = np.array([1.,0.,0.,0.])
		mySat = satellite.Satellite(np.hstack((q,value)),128.05)
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot(mySat,128.08,mySat.getState())

		self.assertTrue(np.allclose(result[4:7],[0.,0.,0.]))

	def test_kinematics_explicitly(self):
		state = np.array([0.4,0.254,-0.508,np.sqrt(1-0.4**2-0.254**2-0.508**2),0.1,-0.05,-0.3])
		mySat = satellite.Satellite(state,128.05)
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([10e-10,0.,0.]))
		mySat.setControl_b(np.array([1e-5,0.,0.]))
		result = x_dot(mySat,128.08,mySat.getState())
		self.assertTrue(np.allclose(result[0:4],[0.082498,0.114183,0.064066,-0.04095]))

	
if __name__=='__main__':
	unittest.main(verbosity=2)