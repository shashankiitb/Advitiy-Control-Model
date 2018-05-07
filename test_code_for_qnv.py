import numpy as np
import qnv

A=[1,2,3]
B=[-1,-2,-3]
C=[1,-2,-3]
D=[4,-6,7]
E=[0,-3,2]
F=[0,0,0]

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
cross=np.array([0,0,0])

G=qnv.cross(A,A)
if (G == cross).all() == 0:
	flag=0

G=qnv.cross(A,B)
if (G == cross).all() == 0:
	flag=0

G=qnv.cross(D,F)
if (G == cross).all() == 0:
	flag=0

G=qnv.cross(D,F)
if (G == cross).all() == 0:
	flag=0

G=qnv.cross(C,D)
cross[0:3]=[-32,-19,2]
if (G == cross).all() == 0:
	flag=0

G=qnv.cross(E,A)
cross[0:3]=[-13,2,3]
if (G == cross).all() == 0:
	flag=0

if flag == 1:
	print ("all cases passed for cross")
else:
	print ("error for cross")