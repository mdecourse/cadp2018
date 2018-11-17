# -*- coding: utf-8 -*-
"""
Robot interface to v-rep
@author: P.Cizek
@version: 3.0
"""
import sys
sys.path.insert(0, "./hexapod_vrep/vrep_api")
import vrep
from . import constants as const
import math
import numpy as np

class Robot:
	#class for interfacing the hexapod robot in V-REP simulator

	def __init__(self):
		self.clientID = self.connect_simulator()
		self.hexapod = None
		self.ref_frame = None
		self.hexa_base = None
		self.servos = []
		self.foot_tips = []
		self.laser_init = True
		self.pos_first = True
		self.orientation_first = True
		self.on_startup()

	#############################################################
	# helper functions for simulator interfacing
	#############################################################
	
	def connect_simulator(self):
		#establish connection to the simulator on localhost
		vrep.simxFinish(-1) # just in case, close all opened connections
		IP_address = "127.0.0.1"
		port = 19997 # port on which runs the continuous remote API
		waitUntilConnected = True
		doNotReconnectOnceDisconnected = True
		timeOutInMs = 5000
		commThreadCycleInMs = 20
		new_clientID = vrep.simxStart(IP_address, port, waitUntilConnected, doNotReconnectOnceDisconnected, timeOutInMs, commThreadCycleInMs)
		if new_clientID!=-1:
			print("Connected to remote API server")
		else:
			print("Connection to remote API server failed")
			sys.exit()
		return new_clientID

	def start_simulation(self):
		#start the simulation
		errorCode = vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)
		assert errorCode == vrep.simx_return_ok, "Simulation could not be started"
		return

	def stop_simulation(self):
		#stop the simulation
		errorCode = vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
		assert errorCode == vrep.simx_return_ok, "Simulation could not be stopped"
		return

	def disconnect_simulator(self):
		#disconnect from the simulator
		vrep.simxFinish(self.clientID)
		return

	def get_object_handle(self, string):
		#provides object handle for V-REP object
		errorCode, handle = vrep.simxGetObjectHandle(self.clientID, string, vrep.simx_opmode_oneshot_wait)
		assert errorCode == vrep.simx_return_ok, "Conection to " + string + "failed"
		return handle

	def get_collision_handle(self, string):
		#provides handle to the collision object in V-REP
		errorCode, handle = vrep.simxGetCollisionHandle(self.clientID, string, vrep.simx_opmode_blocking)
		assert errorCode == vrep.simx_return_ok, "Getting " + string + " handle failed"
		return handle

	def get_collision_state(self, c_handle):
		#getting collision status of object
		errorCode, collisionState=vrep.simxReadCollision(self.clientID, c_handle, vrep.simx_opmode_blocking)
		assert errorCode == vrep.simx_return_ok, "Cannot read collision"
		return collisionState

	def get_servos_handles(self):
		#retrieve servo handles
		servos=[]
		for i in range(1,19):
			servo = self.get_object_handle("hexa_joint" + str(i))
			servos.append(servo)
		return servos

	def get_hexa_base_handle(self):
		#retrieve handle of the robot base
		hexa_base = self.get_object_handle("hexa_base")
		return hexa_base

	def get_foot_tips_handles(self):
		#retrieve handles of the foot tips
		foot_tips = []
		for i in range(1,7):
			foot_tip = self.get_object_handle("hexa_footTip" + str(i))
			foot_tips.append(foot_tip)
		return foot_tips

	def get_hexapod_handle(self):
		#retrieve handle for the hexapod object
		hexapod=self.get_object_handle("hexapod")
		return hexapod
		
	def get_hexapod_collision_handle(self):
		#retrieve handle for the hexapod object
		hexapod=self.get_object_handle("hexapod")
		return hexapod

	def on_startup(self):
		# startup routine
		self.hexapod = self.get_hexapod_handle()
		self.servos = self.get_servos_handles()
		self.hexa_base = self.get_hexa_base_handle()
		self.foot_tips = self.get_foot_tips_handles()
		self.turn_on()
		#start the simulation
		self.start_simulation()
		print("Robot ready")
		return

	#############################################################
	# locomotion helper functions
	#############################################################

	def get_servo_position(self, servoID):
		#getting position of servos
		print(str(servoID))
		assert servoID > 0 and servoID <= 18, "Commanding unexisting servo"
		errorCode, value = vrep.simxGetJointPosition(self.clientID, self.servos[servoID-1], vrep.simx_opmode_blocking)
		assert errorCode == vrep.simx_return_ok, "Failed to read servo position"
		return value

	def set_servo_position(self, servoID, angle):
		#setting position of servos
		assert servoID > 0 and servoID <= 18, "Commanding unexisting servo"
		errorCode = vrep.simxSetJointTargetPosition(self.clientID, self.servos[servoID-1], angle, vrep.simx_opmode_streaming)
		assert errorCode == vrep.simx_return_ok or errorCode == vrep.simx_return_novalue_flag, "Failed to set servo position"

	def turn_on(self):
		#standing up the robot to base position
		for i in range(1,19):
			self.set_servo_position(i, const.SERVOS_BASE[i-1]/180.0*3.141593)

	def get_robot_position(self):
		#get the position of the robot
		if self.pos_first:
			self.pos_first = False
			errorCode, position = vrep.simxGetObjectPosition(self.clientID, self.hexapod, -1, vrep.simx_opmode_streaming) #start streaming
		else:
			errorCode, position = vrep.simxGetObjectPosition(self.clientID, self.hexapod, -1, vrep.simx_opmode_buffer) #fetch new data from stream
		
		if errorCode == vrep.simx_return_novalue_flag:
			position = None
		else:
			assert errorCode == vrep.simx_return_ok, "Cannot get object position" 
		return position

	def get_robot_orientation(self): 
		#get the orientation of the robot
		if self.orientation_first:
			self.orientation_first = False
			errorCode, orientation = vrep.simxGetObjectOrientation(self.clientID, self.hexapod, -1, vrep.simx_opmode_streaming) #start streaming
		else:
			errorCode, orientation = vrep.simxGetObjectOrientation(self.clientID, self.hexapod, -1, vrep.simx_opmode_buffer) #fetch new data from stream
		
		if errorCode == vrep.simx_return_novalue_flag:
			return None
		else:
			assert errorCode == vrep.simx_return_ok, "Cannot get object orientation"
		
		#extract orientation from Euler angles to one angle between 0 and 2pi
		phi = 0
		if orientation[1] < 0:
			if orientation[2] < 0:
				phi = math.pi/2 - orientation[1] 
			else:
				phi = 3*math.pi/2 + orientation[1]
		else:
			if orientation[2] < 0:
				phi = math.pi/2 - orientation[1]
			else:
				phi = 3*math.pi/2 + orientation[1]
		
		return phi

	#############################################################
	# laser scanner sensor interface
	#############################################################

	def get_laser_scan(self):
		ret = None
		#fetch the data from the laser scanner
		if self.laser_init:
			errorCode, signalVal = vrep.simxGetStringSignal(self.clientID, "MySignal", vrep.simx_opmode_streaming) #start streaming
		else:
			errorCode, signalVal = vrep.simxGetStringSignal(self.clientID, "MySignal", vrep.simx_opmode_buffer) #fetch new data from stream
		
		if errorCode == vrep.simx_return_novalue_flag:
			ret = None
		else:
			assert errorCode == vrep.simx_return_ok, "Cannot grab laser data"
		#clear the message queue
		vrep.simxClearStringSignal(self.clientID, "MySignal", vrep.simx_opmode_oneshot)
		
		data = vrep.simxUnpackFloats(signalVal)
		
		scan_x = data[0::2]
		scan_y = data[1::2]
		if len(scan_x) != len(scan_y):
			ret = None
		else:
			ret = (scan_x, scan_y)
		return ret