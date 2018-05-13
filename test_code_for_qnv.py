import numpy as np
import qnv

A=np.array([1,2,3])
B=np.array([-1,-2,-3])
C=np.array([1,-2,-3])
D=np.array([4,-6,7])
E=np.array([0,-3,2])
F=np.array([0,0,0])

flag=1 #to check whether code passes all test cases for dot. flag will be made 0 if it fails any test case

G=qnv.dot(A,A)
if G != 14:
	flag=0

G=qnv.dot(B,B)
if G != 14:
	flag=0

G=qnv.dot(A,B)
if G != -14:
	flag=0

G=qnv.dot(C,D)
if G != -5:
	flag=0

G=qnv.dot(E,A)
if G != 0:
	flag=0

G=qnv.dot(F,E)
if G != 0:
	flag=0

G=qnv.dot(F,F)
if G != 0:
	flag=0

if flag == 1:
	print ("all cases passed for dot")
else:
	print ("error for dot")

flag=1 #to check for cross

G=qnv.cross(A,A)
if (G == F).all() == 0:
	flag=0

G=qnv.cross(A,B)
if (G == F).all() == 0:
	flag=0

G=qnv.cross(D,F)
if (G == F).all() == 0:
	flag=0

G=qnv.cross(D,F)
if (G == F).all() == 0:
	flag=0

G=qnv.cross(C,D)
expected_cross=np.array([-32,-19,2])
if (G == expected_cross).all() == 0:
	flag=0

G=qnv.cross(E,A)
expected_cross[0:3]=[-13,2,3]
if (G == expected_cross).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for cross")
else:
	print ("error for cross")

q1=np.array([1,2,3,4])
q2=np.array([1,-2,-3,-4])
q3=np.array([1,-2,-3,4])
q4=np.array([1,2,3,-4])
q5=np.array([-1,-2,-3,4])
q6=np.array([-1,2,3,-4])
q7=np.array([0,2,-3,0])
q8=np.array([0,-2,3,0])
q9=np.array([0,0,0,0])

flag=1 # tessting for quatInv

G=qnv.quatInv(q1)
if (G == q2).all() == 0:
	flag=0

G=qnv.quatInv(q3)
if (G == q4).all() == 0:
	flag=0

G=qnv.quatInv(q5)
if (G == q6).all() == 0:
	flag=0

G=qnv.quatInv(q7)
if (G == q8).all() == 0:
	flag=0

G=qnv.quatInv(q9)
if (G == q9).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for quatInv")
else:
	print ("error for quatInv")
 
flag=1 # testing for quatMultiplynorm
m1 = np.array([1,-1,-1,1])
m2 = np.array([-1,1,-1,-1])
m3 = np.array([0,1,1,-1])
m4 = np.array([0,1,-1,0])
m5 = np.array([0,0,-1,1])
m6 = np.array([0,4,0,0])
m7 = np.array([-1,-3,-1,-1])
m8 = np.array([-1,-1,-1,-1])
m9 = m6/np.linalg.norm(m6)
m10 = m7/np.linalg.norm(m7)
m11 = m8/np.linalg.norm(m8)

G=qnv.quatMultiplynorm(m1,m2)
if (G == m9).all() == 0:
	flag=0

G=qnv.quatMultiplynorm(m3,m2)
if (G == m10).all() == 0:
	flag=0

G=qnv.quatMultiplynorm(m4,m5)
if (G == m11).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for quatMultiplynorm")
else:
	print ("error for quatMultiplynorm")

flag=1 # testing for quatMultiplynorm

G=qnv.quatMultiplyunnorm(m1,m2)
if (G == m6).all() == 0:
	flag=0

G=qnv.quatMultiplyunnorm(m3,m2)
if (G == m7).all() == 0:
	flag=0

G=qnv.quatMultiplyunnorm(m4,m5)
if (G == m8).all() == 0:
	flag=0

G=qnv.quatMultiplyunnorm(q9,q9)
if (G == q9).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for quatMultiplyunnorm")
else:
	print ("error for quatMultiplyunnorm")
