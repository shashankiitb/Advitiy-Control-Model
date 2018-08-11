import numpy as np
import unittest
import satellite
import frames 
from dynamics import x_dot_BI, x_dot_BO 
from constants_1U import m_INERTIA
from ddt import ddt, data, unpack

@ddt
class TestDynamicsBI(unittest.TestCase):
	def test_zero_torque_rates_ideal_q(self):	#zero torque, zero initial angular velocity, aligned frames
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,0.,0.,0.]),12.0)
		mySat.setPos(np.array([1e6,0.,0.]))
		mySat.setVel(np.array([5.0,5.0,0.0]))
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot_BI(mySat,12.0,mySat.getState())
		self.assertTrue(np.allclose(result,[0.,0.,0.,0.,0.,0.,0.]))

	def test_zero_torque_ideal_q(self):
		mySat = satellite.Satellite(np.array([1.0,0.,0.,0.,-0.1,0.39,-0.7]),12.05)
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot_BI(mySat,12.06,mySat.getState())
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
		result = x_dot_BI(mySat,128.08,mySat.getState())

		self.assertTrue(np.allclose(result[4:7],[0.,0.,0.]))

	def test_kinematics_explicitly(self):
		state = np.array([0.4,0.254,-0.508,np.sqrt(1-0.4**2-0.254**2-0.508**2),0.1,-0.05,-0.3])
		mySat = satellite.Satellite(state,128.05)
		mySat.setPos(np.array([1e6,53e5,0.]))
		mySat.setVel(np.array([5.60,-5.0,0.0]))
		mySat.setDisturbance_b(np.array([10e-10,0.,0.]))
		mySat.setControl_b(np.array([1e-5,0.,0.]))
		result = x_dot_BI(mySat,128.08,mySat.getState())
		self.assertTrue(np.allclose(result[0:4],[0.082498,0.114183,0.064066,-0.04095]))

	print (" dynamics in BI tested ")

@ddt
class TestDynamicsBO(unittest.TestCase):
	def test_zero_torque_rates_ideal_q(self):	#zero torque, zero initial wBIB, aligned frames
		'''
		For this test case set (from sixth model of Advitiy)
		Ixx = 0.00152529
		Iyy = 0.00145111
		Izz = 0.001476
		Ixy = 0.00000437
		Iyz = - 0.00000408
		Ixz = 0.00000118
		'''
		qBO = np.array([1.0,0.,0.,0.])
		pos = np.array([1e6,0.,0.])
		vel = np.array([5.0,5.0,0.0])
		state = np.hstack((qBO,np.array([0.,0.01996437,0.])))
		mySat = satellite.Satellite(state,12.0)
		mySat.setPos(pos)
		mySat.setVel(vel)
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot_BO(mySat,12.0,mySat.getState())
		self.assertTrue(np.allclose(result,[0.,0.,0.009982185,0.,0.,0.,0.]))
		
	def test_zero_torque_ideal_q(self):		#zero torque, random initial angular velocity, aligned frames
		qBO = np.array([1.0,0.,0.,0.])
		pos = np.array([1e6,53e5,0.])
		vel = np.array([5.60,-5.0,0.0])
		state = np.hstack((qBO,np.array([-0.1,0.39159385,-0.7])))
		mySat = satellite.Satellite(state,12.05)
		mySat.setPos(pos)
		mySat.setVel(vel)
		mySat.setDisturbance_b(np.array([0.,0.,0.]))
		mySat.setControl_b(np.array([0.,0.,0.]))
		result = x_dot_BO(mySat,12.06,mySat.getState())
		self.assertTrue(np.allclose(result,[0.,-0.05,0.1957969257,-0.35, 0.00490396,-0.00185206,-0.00173161]))

	def test_kinematics_explicitly(self):
		qBO = np.array([0.4,0.254,-0.508,np.sqrt(1-0.4**2-0.254**2-0.508**2)])
		pos = np.array([1e6,53e5,0.])
		vel = np.array([5.60,-5.0,0.0])
		state = np.hstack((qBO,np.array([0.10050588,-0.05026119,-0.3014887])))
		mySat = satellite.Satellite(state,128.05)
		mySat.setPos(pos)
		mySat.setVel(vel)
		mySat.setDisturbance_b(np.array([10e-10,-4e-6,-3e-5]))
		mySat.setControl_b(np.array([1e-5,1e-5,-8e-4]))
		result = x_dot_BO(mySat,128.08,mySat.getState())
		print(result)
		self.assertTrue(np.allclose(result,[0.08290271,  0.11475622,  0.06438473, -0.04115242,  0.00627683,  0.00299226, -0.56264081]))

print ("dynamics in BO tested")
	
if __name__=='__main__':
	unittest.main(verbosity=2)