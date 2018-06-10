import numpy as np 
import constants_1U as cons

'''
magMoment takes input:
	current magnetic field (Bc) and previous magnetic field (Bp) in body frame (from sensors)
code gives output:
	magnetic moment to be applied in body frame
'''
def magMoment(sat): 
	Bc=sat.getMag_b_m_c()
	Bp=sat.getMag_b_m_p()
	v_magMoment_body=np.zeros([3])
	v_magf_dot_body=(Bc-Bp)/cons.DELAY_STEP
	v_magMoment_body= -cons.k * v_magf_dot_body/np.linalg.norm(Bc)
	return v_magMoment_body