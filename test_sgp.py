import numpy as np
import unittest
import math
import time
import scipy.io
from constants_1U import G,M_EARTH


class TestOrbitData(unittest.TestCase):
	#orbit = 1e3*np.genfromtxt('sgp_output.csv',delimiter = ',')
	orbit = np.genfromtxt('sgp_output.csv', delimiter=",")
	expected_RAAN = 155.9141	#in degrees
	expected_inc = 98.1258	#in degrees
	expected_eccentricity = 0.0032873	
	expected_meanMotion = 14.62910114	#revolutions per day
	expected_argPerigee = 333.2318	#in degrees
	t2 = time.time()
	
	def testRAAN(self):
		x = self.orbit.copy()
		node = np.zeros((1,7))
		for i in range(0,len(x)):
			y1 = x[i,3]
			y2 = x[i+1,3]
			v = x[i,6]
			if y1*y2 < 0 and v >= 0.:
				node = x[i,:].copy()
				break 

		RAAN = np.degrees(math.atan2(node[2],node[1]))
		print node[1:4]
		print RAAN ,"RAAN"
		self.assertAlmostEqual(RAAN,self.expected_RAAN,places=0)

	def testInclination(self):
		x = self.orbit.copy()
		l = np.cross(x[0,1:4],x[0,4:7])/np.linalg.norm(np.cross(x[0,1:4],x[0,4:7]))
		inc = np.degrees(math.acos(l[2]))
		print inc ,"INC"
		self.assertAlmostEqual(inc,self.expected_inc,places=1)
	
	def testEccentricity(self):
		x = self.orbit.copy()
		radius = np.zeros(x.shape[0])
		
		for i in range(0,len(x[:,0])):
			radius[i] = np.linalg.norm(x[i,1:4])
		ecc = (np.amax(radius) - np.amin(radius))/(np.amax(radius) + np.amin(radius))
		print ecc , "ECC"
		
		self.assertAlmostEqual(ecc,self.expected_eccentricity,places=3)
	
	def testMeanMotion(self):
		x = self.orbit.copy()
		radius = np.zeros(x.shape[0])
		for i in range(0,len(x[:,0])):
			radius[i] = np.linalg.norm(x[i,1:4])

		a = 0.5*(np.amax(radius) + np.amin(radius))
		mm = np.sqrt(G*M_EARTH/a**3)*60*60*24/(2*np.pi)
		print x[:,0]
		self.assertAlmostEqual(mm,self.expected_meanMotion,places=2)

	def testArgPerigee(self):
		x = self.orbit.copy()
		node = np.zeros((1,3))
		radius = np.zeros(x.shape[0])
		for i in range(0,len(x[:,0])):
			radius[i] = np.linalg.norm(x[i,1:4])
			y1 = x[i,3]
			if i < len(x[:,0])-1:
				y2 = x[i+1,3]
			else:
				y2 = y1.copy()
			v = x[i,6]
			if y1*y2 < 0 and v >= 0.:
				node = x[i,1:4].copy()
		index = np.argmin(radius)
		e = x[index,1:4]
		print radius[index]
		print node
		w = math.acos(np.dot(node,e)/(np.linalg.norm(node)*np.linalg.norm(e)))
		if e[2] < 0:
			w = 2*np.pi - w
		self.assertAlmostEqual(np.degrees(w),self.expected_argPerigee)		

if __name__=='__main__':
	unittest.main(verbosity=2)