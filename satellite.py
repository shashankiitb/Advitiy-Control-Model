from constants_1U import *
import numpy as np
import qnv
import frames as fs

class Satellite:

	def __init__(self,state0,time0):

		self.setTime(time0)
		self.setState(state0)		

	def setState(self,state1):	#set state

		self.state = state1.copy()

	def getState(self):	#returns the state

		return self.state

	def setPos(self,pos):	#set position in eci (earth centered inertial frame)

		self.v_pos_i = pos.copy()

	def getPos(self):	#return position in eci

		return self.v_pos_i

	def setVel(self,vel):	#set velocity in eci

		self.v_vel_i = vel.copy()

	def getVel(self):	#get velocity in eci

		return self.v_vel_i

	def setQ(self,q):	#set exact quaternion

		self.state[0:4] = q.copy()

	def getQ(self):	#get exact quaternion
		return self.state[0:4]

	def setW(self,omega):	#set angular rate of body wrt ecif in body frame 

		self.state[4:7] = omega.copy()

	def setTime(self,y):	#set time
		self.time = y

	def getTime(self):	#return time
		return self.time

	def setDisturbance_b(self,v_torque_dist_b):	#set disturbance in body (about center of mass)
		self.dist_b = v_torque_dist_b.copy()

	def getDisturbance_b(self):	#return disturbance in body

		return self.dist_b


	def setControl_b(self,v_control_b):	#set control torque in body
		self.control_body = v_control_b.copy()

	def getControl_b(self): #return control torque in body
		return self.control_body

	def setSun_i(self,v_sv_i):	#set sun vector in eci
		self.sv_i = v_sv_i.copy()	

	def setMag_i(self,v_mag_i):	#set mag in eci
		self.mag_i = v_mag_i.copy()

	def getSun_i(self):	#return sun in eci
		return self.sv_i

	def getMag_i(self):	#return mag in eci
		return self.mag_i

	def getSun_o(self):	#get sun vector in orbit
		v_sv_o = fs.ecif2orbit(self.v_pos_i,self.v_vel_i,self.sv_i)
		return	v_sv_o

	def getMag_o(self):	#return mag in orbit
		v_mag_o = fs.ecif2orbit(self.v_pos_i,self.v_vel_i,self.mag_i)
		return	v_mag_o

	def setSun_b_m(self,v_sv_b_m):	#set sunsensor measurement in body
		self.sv_b_m = v_sv_b_m.copy()

	def setMag_b_m(self,v_mag_b_m):	#set mag measurement in body
		self.mag_b_m = v_mag_b_m.copy()

	def getSun_b_m(self):	#return sunsensor measurement in body
		return self.sv_b_m

	def getMag_b_m(self):	#return mag measurement in body
		return self.mag_b_m

	def setQUEST(self,v_q_BO_m):	#set quest quaternion
		self.quatEstimate = v_q_BO_m.copy()

	def getQUEST(self):	#return quest quaternon
		return self.quatEstimate

	def setOmega_m(self,v_w_bob_m):
		self.omega_m = v_w_bob_m.copy()

	def getOmega_m(self):
		return self.omega_m

	def setLight(self,flag):
		self.light = flag

	def getLight(self):
		return self.light

	def getW(self):

		return self.state[4:7]
