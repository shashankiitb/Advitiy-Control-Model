import numpy as np
import matplotlib.pyplot as plt
import qnv
import os
os.chdir('Logs/sso-1U-dist')

time = np.load('time.npy')
v_state = np.load('state.npy')
v_q_BO = np.load('q_BO.npy')
v_w_BOB = np.load('w_BOB.npy')
euler = np.load('euler.npy')
dist_b = np.load('disturbance.npy')
r = np.load('position.npy')
plt.plot(time,euler[:,0],label='roll')
plt.plot(time,euler[:,1],label='pitch')
plt.plot(time,euler[:,2],label='yaw')
plt.ylim(-180,180)
plt.title("euler_BO in degrees")
plt.legend()
plt.show()

plt.plot(time,(180./np.pi)*v_w_BOB[:,0],label='wBOB_x')
plt.plot(time,(180./np.pi)*v_w_BOB[:,1],label='wBOB_y')
plt.plot(time,(180./np.pi)*v_w_BOB[:,2],label='wBOB_z')
plt.title('wBOB in degrees')
plt.legend()
plt.show()

plt.plot(time,v_q_BO[:,0],label='q0')
plt.plot(time,v_q_BO[:,1],label='q1')
plt.plot(time,v_q_BO[:,2],label='q2')
plt.plot(time,v_q_BO[:,3],label='q3')
plt.title('qBO')
plt.legend()
plt.show()

plt.plot(time,r[:,0],label='x')
plt.plot(time,r[:,1],label='y')
plt.plot(time,r[:,2],label='z')
plt.legend()
plt.show()


plt.plot(time,dist_b[:,0],label="t_x")
plt.plot(time,dist_b[:,1],label="t_y")
plt.plot(time,dist_b[:,2],label="t_z")
plt.legend()
plt.title('disturbance torque')
plt.show()


plt.plot(time,v_state[:,0],label='q0')
plt.plot(time,v_state[:,1],label='q1')
plt.plot(time,v_state[:,2],label='q2')
plt.plot(time,v_state[:,3],label='q3')
plt.title("q_BIB")
plt.legend()
plt.show()

plt.plot(time,(180./np.pi)*v_state[:,4],label='wBIBx')
plt.plot(time,(180./np.pi)*v_state[:,5],label='wBIBy')
plt.plot(time,(180./np.pi)*v_state[:,6],label='wBIBz')
plt.title("wBIB in degrees")
plt.legend()
plt.show()


