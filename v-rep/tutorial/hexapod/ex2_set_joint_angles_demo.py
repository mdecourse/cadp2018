import sys
import hexapod_vrep.robot as rob
import time
import math

#instantiate robot
robot = rob.Robot()

time.sleep(0.1)

#define joint angles
servos_angles = [math.pi/6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#set individual servo positions according to robot scheme
#note, servos are numbered from 1 to 18
for i in range(0,18):
	robot.set_servo_position(i+1,servos_angles[i])

#wait before finishing
time.sleep(0.1)

