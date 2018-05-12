import qnv	
import unittest	
import numpy as np
from ddt import ddt,file_data,unpack

@ddt
class Testquatrotate(unittest.TestCase):
	@file_data("test_quatRotate.json")
	@unpack
	def test_quatrotate(self,value):
		  v=np.asarray(value[0])
		  q=np.asarray(value[1])
		  vr=np.asarray(value[2])
		  A=qnv.quatRotate(q,v)
		  
		  self.assertTrue(np.allclose(A,vr))
@ddt
class Testquatrotm(unittest.TestCase):
	@file_data('test_quatrotm.json')
	@unpack
	def test_quat2rotm(self,value):
	        q=np.asarray(value[0])
	        m1=np.asarray(value[1])
	        m2=np.asarray(value[2])
	        m3=np.asarray(value[3])
	        A=qnv.quat2rotm	        
	        self.assertTrue(np.allclose(A[0,:],m1))
	        self.assertTrue(np.allclose(A[1,:],m2))
	        self.assertTrue(np.allclose(A[2,:],m3))
	    	

if __name__=='__main__':
	unittest.main(verbosity=2)