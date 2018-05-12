import numpy as np                                     
from constants_1U import m_INERTIA
from qnv import quatDer1
#-----------------------------------------------------------------------------------------------------------------------------
def x_dot(sat,t,x):    #need m_INERTIA 
    '''
        This function calculates the derivative of quaternion (q_BI)
        and angular velocity w_BIB
    '''
    #get torques acting about COM
    v_torque_control_b = sat.getControl_b()     #Control torque
    v_torque_dist_b = sat.getDisturbance_b()    #Disturbance torque
    v_torque_b = v_torque_control_b + v_torque_dist_b

    #get current state
    v_state = x.copy()
    v_q_BI = v_state[0:4].copy()   #unit quaternion rotating from ecif to body 
    v_w_BIB = v_state[4:7].copy()  #angular velocity of body frame wrt ecif in body frame
    
    #Kinematic equation
    v_q_dot = quatDer1(v_q_BI,v_w_BIB)   
    #Dynamic equation 
    m_INERTIA_inv = np.linalg.inv(m_INERTIA)
    
    v_w_dot = np.dot(m_INERTIA_inv,v_torque_b - np.cross(v_w_BIB,np.dot(m_INERTIA,v_w_BIB)))    #Euler equation of motion

    v_xdot = np.hstack((v_q_dot,v_w_dot))
    
    return v_xdot   

