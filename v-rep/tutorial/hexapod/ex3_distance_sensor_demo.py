import sys
import hexapod_vrep.robot as rob
import time
import pylab as plt

#initialize robot
robot = rob.Robot()
time.sleep(0.1)

#prepare ploting canvas
plt.ion() 
fig=plt.figure()

while True:
	#read distance data
	scan_x,scan_y = robot.get_laser_scan()
	time.sleep(0.1)
	
	#plot the scanned points
	plt.clf() # clear canvas
	plt.plot(scan_x,scan_y,'.-r') #plot scanned points
	plt.axis('equal')
	plt.show()
	plt.pause(0.0001)