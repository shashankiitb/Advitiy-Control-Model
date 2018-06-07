import numpy as np                                     
from constants_1U import m_INERTIA,m_INERTIA_inv
from qnv import quatDer1
#-----------------------------------------------------------------------------------------------------------------------------
def x_dot(sat,t,v_x):    #need m_INERTIA 
    '''
        This function calculates the derivative of quaternion (q_BI)
        and angular velocity w_BIB
        Input: satellite, time, state vector
        Output: Differential state vector
    '''
    #get torques acting about COM
    v_torque_control_b = sat.getControl_b()     #Control torque
    v_torque_dist_b = sat.getDisturbance_b()    #Disturbance torque
    v_torque_b = v_torque_control_b + v_torque_dist_b
    
    #get current state
    v_state = v_x.copy()
    v_q_BI = v_state[0:4].copy()   #unit quaternion rotating from ecif to body 
    v_w_BI_b = v_state[4:7].copy()  #angular velocity of body frame wrt ecif in body frame
    
    #Kinematic equation
    v_q_dot = quatDer1(v_q_BI,v_w_BI_b)   
    #Dynamic equation 
   
    
    v_w_dot = np.dot(m_INERTIA_inv,v_torque_b - np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b)))    #Euler equation of motion

    v_x_dot = np.hstack((v_q_dot,v_w_dot))
    
    return v_x_dot   

