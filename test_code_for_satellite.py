import Satellite as Sat
import numpy as np
import qnv
import frames as fs

state1[0:4]=np.array([1,0,0,0,10,0,0,0]) 
state2[0:4]=np.array([2,0,0,0,20,0,0,0])
state3[0:4]=np.array([1.1,0.1,0.1,0.1,10,0,0,0])
state4[0:4]=np.array([1.2,0.2,0.2,0.2,20,0,0,0])

#Case1: initializing with integer and reseting to integer

Sat1 = Satellite(state1,0)

a=Sat1.getState()

if (a == state1):
	print "_init_ and getState correct"
else:
	print "_init_ or getState incorrect"

t=Sat1.getTime()
if(t==0):
	print "_init_ and getTime correct"
else:
	print "_init_ or getTime incorrect"

t=Sat1.setTime(1)
t=Sat1.getTime()
if (t == 1):
	print "setTime and getTime correct"
else:
	print "setTime or getTime incorrect"

Sat1.setState(state2)
a=Sat1.getState()

if (a == state2):
	print "setState correct"
else:
	print "setState incorrect"

#Case2: initializing with integer and reseting to float
Sat2 = Satellite(state1,0)

t=Sat2.setTime(0.1)
t=Sat2.getTime()
if (t == 0.1):
	print "setTime or getTime correct"
else:
	print "setTime or getTime incorrect"
Sat2.setState(state3)
a=Sat2.getState()

if (a == state3):
	print "setState correct"
else:
	print "setState incorrect"

#Case3: initializing with float and reseting to integer

Sat3 = Satellite(state3,0.1)

a=Sat3.getState()

if (a == state3):
	print "_init_ and getState correct"
else:
	print "_init_ or getState incorrect"

t=Sat3.getTime()
if(t==0.1):
	print "_init_ and getTime correct"
else:
	print "_init_ or getTime incorrect"

t=Sat3.setTime(1)
t=Sat3.getTime()
if (t == 1):
	print "setTime and getTime correct"
else:
	print "setTime or getTime incorrect"
Sat3.setState(state1)
a=Sat3.getState()

if (a == state1):
	print "setState correct"
else:
	print "setState incorrect"

#Case4: initializing with float and reseting to float
Sat4 = Satellite(state3,0.1)
t=Sat4.setTime(0.2)
t=Sat4.getTime()
if (t == 0.2):
	print "setTime correct"
else:
	print "setTime incorrect"
Sat4.setState(state4)
a=Sat4.getState()

if (a == state4):
	print "setState correct"
else:
	print "setState incorrect"

Sat4.setPos(state2)
v_Pos_i=Sat4.getPos()

if (v_Pos_i == state2):
	print "setPos or getPos correct"
else:
	print "setPos or getPos incorrect"

Sat4.setVel(state1)
v_vel_i=Sat4.getVel()

if (v_vel_i == state2):
	print "setPos or getPos correct"
else:
	print "setPos or getPos incorrect"

Sat4.setQ(state4)
Q=Sat4.getQ()

if (Q==state4):
	print "setQ and getQ correct"
else:
	print "setQ and getQ incorrect"

Sat4.setW(state3)
a=Sat4.getW()

if (a==state3):
	print "setW and getW correct"
else:
	print "setW and getW incorrect"

Sat4.setDisturbance_i(state2)
a=getDisturbance_b()
v_t_d_o=fs.ecif2orbit(v_Pos_i,v_vel_i,state2)
b=qnv.quatRotate(Q,v_t_d_o)
if (a==b):
	print "setDisturbance_i and getDisturbance_b correct"
else:
	print "setDisturbance_i or getDisturbance_b incorrect"

Sat4.setControl_b(state1)
a=Sat4.getControl_b()
if (a==state1):
	print "setControl and getControl correct"
else:
	print "setControl and getControl incorrect"

Sat4.setSun_i(state4)
sv_i=Sat4.getSun_i()
if (sv_i==state4):
	print "setSun_i and getSun_i correct"
else:
	print "setSun_i and getSun_i incorrect"

Sat4.setMag_i(state3)
mag_i=getMag_i()
if (mag_i==state3):
	print "setMag_i and getMag_i correct"
else:
	print "setMag_i and getMag_i incorrect"

a=Sat4.getSun_o()
b=fs.ecif2orbit(v_Pos_i,v_vel_i,sv_i)
if (a==b):
	print "getSun_o correct"
else:
	print "getSun_o incorrect"

a=Sat4.getMag_o()
b=fs.ecif2orbit(v_Pos_i,v_vel_i,mag_i)
if (a==b)
	print "getMag_o correct"
else:
	print "getMag_o incorrect"

Sat4.setSun_b_m(state2)
a=Sat4.getSun_b_m()
if (a==state2):
	print "setSun_b_m and getSun_b_m correct"
else:
	print "setSun_b_m and getSun_b_m incorrect"

Sat4.setMag_b_m(state1)
a=Sat4.getMag_b_m()
if (a==state1):
	print "setMag_b_m and getMag_b_m correct"
else:
	print "setMag_b_m and getMag_b_m incorrect"

Sat4.setQuest(state4)
a=getQuest()
if (a==state4):
	print "setQuest and getQuest correct"
else:
	print "setQuest and getQuest incorrect"

Sat4.setOmega_m(state3)
a=getOmega_m()
if (a==state3):
	print "setOmega_m and getOmega_m correct"
else:
	print "setOmega_m and getOmega_m incorrect"

Sat4.setLight(1)
if (Sat4.light==1):
	print "setLight correct"
else:
	print "setLight incorrect"