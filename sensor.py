import numpy as np
from constants import *

def sunsensor(v_sv_b):
	return v_sv_b + ss_error

def magmeter(v_mag_b):
	return v_mag_b + mag_error

def gyro(v_w_bob):
	return v_w_bob + gyro_error

