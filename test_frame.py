import frames as fr 	#module to be tested
import unittest	#testing library
import numpy as np

class TestFrameConversions(unittest.TestCase):
	def test_latlon(self):
		x = np.array([1.,0.,0.])
		y = fr.latlon(x)	#y is tuple
		lat = y[0]
		lon = y[1]
		self.assertEqual(lat,0.0)
		self.assertEqual(lon,0.0)




if __name__=='__main__':
	unittest.main()