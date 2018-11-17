from numpy import array
import numpy as np
import math

#				1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18
SERVOS_BASE = [	0, 0, -30, 30, 60,-60,  0,  0,-30,  30, 60,-60,	 0,  0,-30, 30, 60,-60]
SERVOS_MINS = [1, 1]
SERVOS_MAXS = [1, 1]


#cpg gait constants
COXA_SERVOS = [1,13,7,2,14,8]
COXA_OFFSETS = [math.pi/8,0,-math.pi/8,-math.pi/8,0,math.pi/8]
FEMUR_SERVOS = [3,15,9,4,16,10]
FEMUR_OFFSETS = [-math.pi/6,-math.pi/6,-math.pi/6,math.pi/6,math.pi/6,math.pi/6]
TIBIA_SERVOS = [5,17,11,6,18,12]
TIBIA_OFFSETS = [math.pi/3,math.pi/3,math.pi/3,-math.pi/3,-math.pi/3,-math.pi/3]
SIGN_SERVOS = [-1,-1,-1,1,1,1]

FEMUR_MAX = 2.1
TIBIA_MAX = 0.1
COXA_MAX = 0.005