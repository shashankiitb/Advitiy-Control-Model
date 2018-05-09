#Code for transformation of vector from one reference frame to another

import numpy as np
from constants_1U import W_EARTH, LAUNCHDAY, EQUINOX
from math import radians, sin, cos, acos, pi


def latlon(x):
	#get the latitude and longitude in degrees given position in ECEF 
	#x is position in ecif
	#latitude ranges [0,90] in north hemisphere and [0,-90] in south hemisphere
	lat=sgn(x[2])*(acos(((x[0]**2+x[1]**2)**0.5)/((x[0]**2+x[1]**2+x[2]**2)**0.5)))*90./(pi/2.) 
       
	# longitude calculation given position, lon is longitude
	#ranges from (-pi,pi]
	if x[1]==0:
		if x[0]>=0 :
			lon = 0.0
		else:
			lon = 180.0

	else:
		lon=sgn(x[1])*acos(x[0]/((x[0]**2+x[1]**2)**0.5))*90./(pi/2)     #x,y,z>0 

	#x axis is intersection of 0 longitude and 0 latitutde

	return lat,lon

def sgn(x):
	#signum function
	if(x==0):
		y = 0
	elif (x>0):
		y = 1
	else:
		y = -1

	return y

def ecif2ecef(x,t):
	#rotate vector in ecif to ecef
	# time t in seconds
	ut_sec = (LAUNCHDAY - EQUINOX).total_seconds() + t # universal time vector in sec 
	theta = W_EARTH*ut_sec #in radian
	DCM = np.array([[cos(theta), sin(theta), 0.], [-1*sin(theta), cos(theta),0.], [0.,0.,1.]])
	y = np.dot(DCM,x)
	
	return y

def ecif2ecefR(today,equinox,t):

	ut_sec = (LAUNCHDAY - EQUINOX).total_seconds() + t # universal time vector in sec
	st_sec = steprut*ut_sec   #sidereal time vector in sec

	phi = st_sec*W_EARTH           # sidereal time vector in rad

	TEI = np.array([[cos(phi),sin(phi),0.],[-sin(phi),cos(phi),0.],[0.,0.,1.]])

	return TEI


def ecef2ecif(x,t):
	#rotate vector from ecef to ecif
	ut_sec = (LAUNCHDAY - EQUINOX).total_seconds() + t # universal time vector in sec
	theta = W_EARTH*ut_sec #in radian
	DCM = np.array([[cos(theta), -1*sin(theta), 0.], [sin(theta), cos(theta),0.],[ 0.,0.,1.]])
	y = np.dot(DCM,x)
	
	return y



def ecif2orbit(r,v,vector_ecif):
	#r is position in eci frame
	#v is velocity in eci frame
    z = -r/np.linalg.norm(r)
    y = np.cross(v,r)/np.linalg.norm(np.cross(v,r))
    x = np.cross(y,z)
    Rot_mat=np.array([x,y,z])
    
    u = np.dot(Rot_mat,vector_ecif)
    
    return u


'''

def ned2ecef(x,lat,lon):
	#rotate vector from North-East-Down frame to ecef
	# lat should be -90 to 90
	# lon should be 0 to 360
	v = np.array([-x[2], -x[0], x[1]]) #convert to spherical polar r theta phi
    
	theta = -lat + 90. #in degree, polar angle (co-latitude)
	phi = lon #in degree, azimuthal angle
	theta = radians(theta)
	phi = radians(phi)

	DCM = np.array([[sin(theta)*cos(phi), cos(theta)*cos(phi), -sin(phi)],\
		[sin(theta)*sin(phi), cos(theta)*sin(phi), cos(phi)],\
		[cos(theta), -sin(theta), 0.]]) #for spherical to cartesian

	y = np.dot(DCM,v)

	return y

'''