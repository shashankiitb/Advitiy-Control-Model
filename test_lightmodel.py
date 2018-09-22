#import lightmodel as lm 	#module to be tested
import unittest	#testing library
import numpy as np
from ddt import ddt,file_data,unpack,data

m_test_lightmodel_output = np.genfromtxt(r'E:\Student Satellite\Control Stuff and Feb 2018 onwards\CLS\Advitiy-Control-Model-detumbling\light_output.csv', delimiter=',')

@ddt
class TestAdd(unittest.TestCase):
	@file_data("test-data/test_lightmodel.json")	#File can contain nested list 
	#first and second number in each sub-list are numbers to be added and third number is expected result
	def test_cases_file(self,value):
		time = value[0]
		expected = value[1]
		result = m_test_lightmodel_output[time*10,1] #Time interval is 0.1sec, so index is time*10 
		print expected, result
		self.assertTrue(np.allclose(result,expected))	
		

if __name__=='__main__':
	unittest.main(verbosity=2)