from satellite import Satellite
import math as mt
import numpy as np
#r1=[1,0,0]
#r2=[1,1,0]    #test case
#b1=[0,1,0]
#b2=[0,1,1]
def quest(sat):
	#q_bob = np.zeros(4)
    r1=sat.getSun_o()	#sun vector in orbit frame
    r2=sat.getMag_o()  #magnetic vector in orbit frame
    b1=sat.getSun_b_m()  #sun vector in body frame
    b2=sat.getMag_b_m()  #magnetic vector in body frame
    
    a1=0.1  #weight of sun vector
    a2=0.9  #weight of magnetic vector
    r=np.cross(r1,r2)
    if r.all()==0:
        x=1;
    else:
        x=np.linalg.norm(r)
    r3=r/x              #define r3
    
    b=np.cross(b1,b2)
    if b.all()==0:
        y=1;
    else:
        y=np.linalg.norm(b)
    b3=b/y              #define b3
    
    p=np.cross(b3,r3)
    q=np.dot(b3,r3)
    r=a1*np.cross(b1,r1)
    s=a2*np.cross(b2,r2)
    rd=a1*np.dot(b1,r1)
    sd=a2*np.dot(b2,r2)
    
    alpha=(1+q)*(rd+sd)+np.dot(p,(r+s))
    beta=np.dot((b3+r3),(r+s))
    gamma=mt.sqrt((alpha**2)+(beta**2))
    q_bob = np.zeros(4)
    if alpha>0:      #for alpha less than 0
        coef1=0.5/mt.sqrt(gamma*(gamma+alpha)*(1+q)) #normalising factor
        q_0=coef1*(gamma+alpha)*(1+q)      #scalar 
        q_v=((gamma+alpha)*p)+(beta*(b3+r3))
        q_1=coef1*q_v[0]     #vector
        q_2=coef1*q_v[1]
        q_3=coef1*q_v[2]
        q_bob[0] = q_0
        q_bob[1] = q_1
        q_bob[2] = q_2
        q_bob[3] = q_3
        
        
       
    if alpha<=0:    #for alpha greater than or equals 0
        coef2=0.5/mt.sqrt(gamma*(gamma-alpha)*(1+q))  #normalising factor
        q_0=coef2*beta*(1+q)     #scalar
        q_v=((beta)*p)+((gamma-alpha)*(b3+r3))
        q_1=coef2*q_v[0]    #vector
        q_2=coef2*q_v[1]
        q_3=coef2*q_v[2]
        q_bob[0] = q_0
        q_bob[1] = q_1
        q_bob[2] = q_2
        q_bob[3] = q_3

    return q_bob
#print(quest(r1,r2,b1,b2))    #to check test case
    
    
    
