import numpy as np                                     
from constants_1U import m_INERTIA,m_INERTIA_inv
from qnv import quatDer1
#-----------------------------------------------------------------------------------------------------------------------------
def x_dot_BI(sat,t,v_x):    #need m_INERTIA 
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
    v_q_dot = quatDerBI(v_q_BI,v_w_BI_b)   
    
    #Dynamic equation 
    v_w_dot = np.dot(m_INERTIA_inv,v_torque_b - np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b)))    #Euler equation of motion

    v_x_dot = np.hstack((v_q_dot,v_w_dot))
    
    return v_x_dot   

def x_dot_BO(sat,t,v_x):    #need m_INERTIA 
    '''
        This function calculates the derivative of quaternion (q_BO)
        and angular velocity w_BOB
        Input: satellite, time, state vector
        Output: Differential state vector
    '''
    #get torques acting about COM
    v_torque_control_b = sat.getControl_b()     #Control torque
    v_torque_dist_b = sat.getDisturbance_b()    #Disturbance torque
    v_torque_b = v_torque_control_b + v_torque_dist_b
    
    #get current state
    v_state = v_x.copy()
    v_q_BO = sat.getqBO()   #unit quaternion rotating from ecif to body 
    v_w_BI_b = v_state[4:7].copy()  #angular velocity of body frame wrt ecif in body frame
    v_w_BO_b = sat.getOmega_m() #angular velocity of body frame wrt orbit frame in body frame
    R = quat2rotm(v_q_BO)
    omega1 = v_w_BI_b - np.matmul(R,v_w_BO_b)
    #Kinematic equation
    v_q_dot = quatDerBO(v_q_BO,omega1)   
   
    #Dynamic equation - Euler equation of motion
    v_w_dot = np.dot(m_INERTIA_inv,v_torque_b - np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b))) - np.matmul(R, (np.cross(omega1, v_w_BO_b) + v_w_BO_b_dot))   

    v_x_dot = np.hstack((v_q_dot,v_w_dot))
    
    return v_x_dot   