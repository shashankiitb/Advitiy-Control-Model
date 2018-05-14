import numpy as np
import constants_1U as constants
import qnv as qnv
import satellite as satellite

'''
this function takes input:
    position of centre of mass of satellite in eci frame
    quarternion to convert vector in eci frame to body frame
    inertia matrix of satellite
             gives output:
    torque due to gravity gradient about centre of mass in body frame
'''


def gg_torque(s):
    q = s.getQ()
    v_pos_sat_i = s.getPos()
    v_pos_sat_b = qnv.quatRotate(q, v_pos_sat_i)
    pos_norm = np.linalg.norm(v_pos_sat_b)
    m_inertia = constants.m_INERTIA  # moment of inertia matrix in body frame
    m = constants.M_EARTH
    g = constants.G
    
    v_t_gg_b = 3 * m * g * (np.cross(v_pos_sat_b, np.dot(m_inertia, v_pos_sat_b))) / pos_norm ** 5
 
    return v_t_gg_b


'''
this function takes input:
    velocity of COM of satellite in eci frame
    quarternion to convert a vector in eci frame to body frame
    vector between COM and geometric centre expressed in body frame
              gives output:
    torque due to air drag about COM in body frame
'''


def aero_torque(s):
    q = s.getQ()
    
    v_vel_sat_i = s.getVel()
    v_pos_i = s.getPos()
    v_vel_atm_i = np.cross(np.array([0.,0.,constants.W_EARTH]),np.array([v_pos_i[0],v_pos_i[1],0.]))    #velocity of atmosphere in eci
    v_vel_i = v_vel_sat_i - v_vel_atm_i #velocity of satellite wrt atmosphere in eci 
    
    v_vel_b = qnv.quatRotate(q, v_vel_i)

    r_com = constants.r_COM  # vector containing coordinates of COM of satellite in body frame
    cd = constants.AERO_DRAG  # aerodynamic drag coefficient of satellite
    rho = constants.RHO  # density of atmosphere at low earth orbit
    vel_norm = np.linalg.norm(v_vel_b)
   
    l = constants.Lx  # length of cube 
    area = l * l * (abs(v_vel_b[0]) + abs(v_vel_b[1]) + abs(v_vel_b[2]))  # area of satellite perpendicular to velocity
    v_t_ad_b = np.cross(r_com, v_vel_b) * rho * cd * vel_norm * area / 2.

    return v_t_ad_b


'''
this function takes input:
    sun vector in eci frame
    quarternion to convert a vector in eci frame to body frame
    vector between COM and geometric centre expressed in body frame
              gives output:
    torque due to solar drag about COM in body frame
'''


def solar_torque(s):
    q = s.getQ()
   
    r_com = constants.r_COM
    e = constants.REFLECTIVITY  # coefficient of reflectivity of satellite
    p = constants.SOLAR_PRESSURE  # solar radiation pressure at low earth orbit
    v_sv_i = s.getSun_i()  # unit sun vector in inertial frame obtained from satellite object
    v_sv_b_u = qnv.quatRotate(q, v_sv_i) / np.linalg.norm(v_sv_i)

    l = constants.Lx
    area = l * l * (abs(v_sv_b_u[0]) + abs(v_sv_b_u[1]) + abs(v_sv_b_u[2]))
    # area of satellite perpendicular to sun vector
    v_t_sd1_b = np.cross(r_com, v_sv_b_u) * p * (1 - e) * area  # torque due to absorption
    v_t_sd2_b = np.cross(r_com, [abs(v_sv_b_u[0]) * v_sv_b_u[0], abs(v_sv_b_u[1]) * v_sv_b_u[1], abs(v_sv_b_u[2]) * v_sv_b_u[2]]) * 2 * e * p * l * l
    # reflection torque
    v_t_sd_b = v_t_sd1_b + v_t_sd2_b

    return v_t_sd_b
