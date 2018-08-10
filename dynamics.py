import numpy as np                                     
from constants_1U import m_INERTIA,m_INERTIA_inv, G, M_EARTH
from qnv import quatDerBI, quat2rotm, quatDerBO
import frames
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
        Input: satellite, time, v_x = row vector consisting of q_BO and w_BOB
        Output: Differential state vector
    '''
    #get torques acting about COM
    v_torque_control_b = sat.getControl_b()     #Control torque
    v_torque_dist_b = sat.getDisturbance_b()    #Disturbance torque
    v_torque_b = v_torque_control_b + v_torque_dist_b
    
    #get current state
    v_q_BO = v_x[0:4]  #unit quaternion rotating from ecif to body 
    v_w_BO_b = v_x[4:7].copy()  #angular velocity of body frame wrt ecif in body frame
    r=np.linalg.norm(sat.getPos())
    v_w_IO_o = np.array([0., np.sqrt(G*M_EARTH/(r)**3), 0.]) #angular velocity of orbit frame wrt inertial frame in orbit frame
    R = quat2rotm(v_q_BO)
    #Kinematic equation
    v_q_BO_dot = quatDerBO(v_q_BO,v_w_BO_b)   
    v_w_BI_b = frames.wBOb2wBIb(v_w_BO_b,v_q_BO,v_w_IO_o)
    v_w_OI_o = -v_w_IO_o.copy()

    #Dynamic equation - Euler equation of motion
    v_w_BO_b_dot = np.dot(m_INERTIA_inv,v_torque_b - np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b))) - np.matmul(R, (np.cross(v_w_BO_b, v_w_OI_o))) 
    print(np.matmul(R, (np.cross(v_w_BO_b, v_w_OI_o)))) 
    print(np.dot(m_INERTIA_inv,np.cross(v_w_BI_b,np.dot(m_INERTIA,v_w_BI_b))))
    v_x_dot = np.hstack((v_q_BO_dot,v_w_BO_b_dot))
    
    return v_x_dot   