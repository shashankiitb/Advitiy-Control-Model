
import numpy as np
from pylab import *
from satellite import Satellite

def controlLaw (sat, dt):
    '''
the function takes input: 
normalised quaternion rotating a vector from body frame to orbit frame
angular velocity of body frame wrt to orbit frame in body frame
measured magnetic field in body frame
gives output:
current to be applied in magnetorquers
here:
q_BO = [qs qv(in body frame)]
dt is time step
q_BO is normalised
assumed that magnetorquers are perfectly aligned with body frame axes
    '''
    q_bo = sat.getQUEST()
    v_w_bo_b_m = sat.getOmega_m()
    v_b_b_m = sat.getMag_b_m()
    print "mag_vec" , v_b_b_m
    N=[1,1,1]                                 #[number of turns of magnetorquer aligned with x axis of body frame, " y axis ", " z axis "]
    A=[1,1,1]                                 #[area of magnetorquer aligned with x axis of body frame, " y axis ", " z axis "]
    m_Kp = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    m_Ki = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    m_Kd = np.array([[ -1,  0,  0], 
                   [  0, -1,  0], 
                   [  0,  0, -1]])
    v_e_b=np.array([])                          #error term in body frame (sin(theta)*UnitVectorOfAxisOfRotation)
    v_ie_b=np.array([0,0,0])                    #integral term
    Bmodsq=(v_b_b_m[0])**2 + (v_b_b_m[1])**2 + (v_b_b_m[2])**2 
    for i in range (0,3,1):
        v_e_b=np.append(v_e_b,[2*q_bo[0]*q_bo[i+1]])
        v_ie_b[i]=v_ie_b[i]+v_e_b[i]*dt
    v_m=(m_Kp.dot(v_e_b)+m_Ki.dot(v_ie_b)+m_Kd.dot(v_w_bo_b_m))/Bmodsq   #PID control 
    v_mControl=np.cross(v_m,v_b_b_m)                #magnetic moment to be applied
    v_I=(v_mControl/A)/N                            #[current to be applied in magnetorquer aligned with x axis of body frame," y axis ", " z axis "]
    return v_I
#controlLaw([1,1,1,1],[0,0,0],[-1,0,1],1)