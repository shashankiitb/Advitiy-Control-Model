from constants import *
import numpy as np
import qnv
import frames as fs

class Satellite:

	def __init__(self,state0,time0):

		self.time = time0
		self.setState(state0)		
		print "init"

	def setState(self,state):	#set state

		self.state = state.copy()

	def getState(self):	#returns the state

		return self.state

	def setPos(self,pos):	#set position in eci

		self.v_pos_i = pos

	def getPos(self):	#return position in eci

		return self.v_pos_i

	def setVel(self,vel):	#set velocity in eci

		self.v_vel_i = vel

	def getVel(self):	#get velocity in eci

		return self.v_vel_i

	def setQ(self,q):	#set exact quaternion

		self.state[0:3] = q.copy()

	def getQ(self):	#get exact quaternion	

		return self.state[0:3]

	def getQi(self):

		return self.qi

	def setW(self,omega):	#set omega

		self.state[4:6] = omega.copy()

	def setTime(self,y):	#set time
		self.time = t

	def getTime(self):	#return time
		return self.time

	def setDisturbance_i(self,v_torque_dist_i):	#set disturbance in eci
		self.dist_i = v_torque_dist_i.copy()

	def getDisturbance_b(self):	#return disturbance in body
		v_t_d_o = ecif2orbit(self.v_pos_i,self.v_vel_i,self.dist_i)	#@Ram
		v_t_d_b = quatRotate(self.state[0:3],v_t_d_o)
		return v_t_d_b

	def setControl_b(self,v_control_b):	#set control torque in body
		self.control_body = v_control_b.copy()

	def getControl_b(self): #return control torque in body
		return self.control_body

	def setSun_i(v_sv_i):	#set sun vector in eci
		self.sv_i = v_sv_i.copy()	

	def setMag_i(v_mag_i):	#set mag in eci
		self.mag_i = v_mag_i.copy()

	def getSun_i():	#return sun in eci
		return self.sv_i

	def getMag_i():	#return mag in eci
		return self.mag_i

	def getSun_o():	#get sun vector in orbit
		v_sv_o = ecif2orbit(self.v_pos_i,self.v_vel_i,self.sv_i)
		return	v_sv_o

	def getMag_o():	#return mag in orbit
		v_mag_o = ecif2orbit(self.v_pos_i,self.v_vel_i,self.mag_i)
		return	v_mag_o

	def setSun_b_m(v_sv_b_m):	#set sunsensor measurement in body
		self.sv_b_m = v_sv_b_m.copy()

	def setMag_b_m(v_mag_b_m):	#set mag measurement in body
		self.mag_b_m = v_mag_b_m()

	def getSun_b_m():	#return sunsensor measurement in body
		return self.sv_b_m

	def getMag_b_m():	#return mag measurement in body
		return self.mag_b_m

	def setQUEST(v_q_BO_m)	#set quest quaternion
		self.quatEstimate = v_q_BO_m.copy()

	def getQUEST()	#return quest quaternon
		return self.quatEstimate





'''
	def getW(self):

		return self.state[10:13]

	def getEnergy(self):
		pos = self.getPos()
		v = self.getVel()
		omega = self.getW()
		T = 0.5*Ms*(np.linalg.norm(v))**2 - G*M*(Ms + mu_m*L/(np.linalg.norm(pos)) + 0.5*np.dot(omega, np.matmul(m_Inertia,omega)))

	def setEmf(self,e):

		self.emf = e

	def getEmf(self):
		
		return self.emf

	
'''