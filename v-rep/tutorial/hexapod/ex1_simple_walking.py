# -*- coding: utf-8 -*-
"""
@author: P.Cizek
"""
import sys
import oscilator_network as osc
import oscilator_constants as const
import hexapod_vrep.robot as rob
import hexapod_vrep.constants as rc
import time
import math
import _thread as thread

def locomotion():
	#cpg oscillator instantiation
	cpg = osc.OscilatorNetwork()
	cpg.change_gait(const.TRIPOD_GAIT_WEIGHTS)
	
	coxa_angles= [0,0,0,0,0,0]
	cycle_length = [0,0,0,0,0,0]
	
	#steering commands
	global left_t
	global right_t
	left = left_t
	right = right_t
	
	#main locomotion control loop
	global stop
	while stop == False:
		
		# steering - acquire left and right steering speeds
		Lock.acquire()
		left = left_t
		right = right_t
		Lock.release()
		coxa_dir = [left,left,left,right,right,right]	#set directions for individual legs

		#next step of CPG
		cycle = cpg.oscilate_all_CPGs()
		#read the state of the network
		data = cpg.get_last_values()

		#reset coxa angles if new cycle is detected
		for i in range(0,6):
			cycle_length[i] += 1;
			if cycle[i] == True:
				coxa_angles[i]= -((cycle_length[i]-2)/2)*rc.COXA_MAX
				cycle_length[i] = 0

		#calculate individual joint angles for each of six legs
		for i in range(0,6):
			femur_val = rc.FEMUR_MAX*data[i] #calculation of femur angle
			if femur_val < 0:
				coxa_angles[i] += coxa_dir[i]*rc.COXA_MAX	#calculation of coxa angle -> stride phase
				femur_val *= 0.1
			else:
				coxa_angles[i] -= coxa_dir[i]*rc.COXA_MAX	#calculation of coxa angle -> stance phase
			
			coxa_val = coxa_angles[i]
			tibia_val = -rc.TIBIA_MAX*data[i]	#calculation of tibia angle
			
			#set position of each servo
			robot.set_servo_position(rc.COXA_SERVOS[i], rc.SIGN_SERVOS[i]*coxa_val+rc.COXA_OFFSETS[i])
			robot.set_servo_position(rc.FEMUR_SERVOS[i],rc.SIGN_SERVOS[i]*femur_val+rc.FEMUR_OFFSETS[i])
			robot.set_servo_position(rc.TIBIA_SERVOS[i],rc.SIGN_SERVOS[i]*tibia_val+rc.TIBIA_OFFSETS[i])
			
			#simulation step time
			time.sleep(0.001)
	
	thread.exit_thread()
	return

if __name__ == "__main__":
	#instantiate robot
	robot = rob.Robot()

	#define global variables used for the robot control
	Lock = thread.allocate_lock()	#mutex for access to turn commands
	l = 1	#left turning speed from interval <-1,1>
	r = 1	#right turning speed from interval <-1,1>
	global left_t
	global right_t
	left_t = l
	right_t = r

	global stop	#global variable to terminate the locomotion thread
	stop = False

	#join walking thread - comply to the hierarchical architecture where robot cintrol is on the bottom level
	try:
		thread1 = thread.start_new_thread(locomotion, ())
	except:
		print("Error: unable to start new thread")

	#wait 10 seconds and then turn off
	time.sleep(10)
	stop = True

	#stop the simulation and disconnect from simulator
	robot.stop_simulation()
	robot.disconnect_simulator()
	sys.exit()