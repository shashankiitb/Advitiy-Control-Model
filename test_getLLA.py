import numpy as np
from constants_1U import EPOCH, EQUINOX, W_EARTH, R_EARTH
from ddt import ddt, data, unpack
import unittest

'''
	This is test code for checking GetLLA output csv file. 
'''

@ddt
class Test_GetLLA(unittest.TestCase):
	sgp_output = np.genfromtxt('sgp_output.csv',delimiter=",")	
	LLA = np.genfromtxt('LLA.csv',delimiter=",")	
	t0 = (EPOCH - EQUINOX).total_seconds()
	T = sgp_output[:,0]
	LLAdata = np.zeros(3)
	def calculate_LLA(self,sgpdata):
		theta = W_EARTH*(self.t0 + sgpdata[0]) #in radian
		m_DCM = np.array([[cos(theta), sin(theta), 0.], [-1*sin(theta), cos(theta),0.], [0.,0.,1.]])
		v_x_e = np.dot(m_DCM,sgpdata[1:4])
		if (v_x_e[2] >= 0):
			LLAdata[0] = acos(((v_x_e[0]**2 + v_x_e[1]**2)/(v_x_e[0]**2 + v_x_e[1]**2 + v_x_e[2]**2))**0.5) * 180./pi
		else:
			LLAdata[0] = -acos(((v_x_e[0]**2 + v_x_e[1]**2)/(v_x_e[0]**2 + v_x_e[1]**2 + v_x_e[2]**2))**0.5) * 180./pi		

		if (v_x[1]==0):
			if (v_x[0]>=0):
				LLAdata[1] = 0.0
			else:
				LLAdata[1] = 180.0
		else:
			if (v_x_e[1] >= 0):
				LLAdata[1] = acos(v_x[0]/((v_x[0]**2 + v_x[1]**2)**0.5))*90./(pi/2)  
			else:
				LLAdata[1] = -acos(v_x[0]/((v_x[0]**2 + v_x[1]**2)**0.5))*90./(pi/2) 

		LLAdata[2] = np.linalg.norm(sgpdata[1:4]) - R_EARTH
		return LLAdata
	
	l = np.linspace(0,len(T),12,int)	#Sample  data points from entire file
	@data(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9])
	
	def test_GetLLA_data(self,value):

		v_expected = self.calculate_LLA(self.sgp_output[value])
		v_result = self.LLA[value,1:4]
		
		self.assertTrue(np.allclose(v_expected,v_result))

if __name__=='__main__':
   unittest.main(verbosity=2)
