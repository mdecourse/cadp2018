# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 23:34:02 2016

@author: fdiacobe
"""

import vrep
import numpy as np
import time
import math
import sys
import matplotlib.pyplot as mlp # to view the camera

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
print(clientID) # if 1, then we are connected.
if clientID!=-1:
    print ("Connected to remote Api server")
else:
    print("Not connected to remote Api server")
    sys.exit("Could not connect")
    
err_code,l_motor_handle = vrep.simxGetObjectHandle(clientID,"ePuck_leftJoint", vrep.simx_opmode_blocking)
err_code,r_motor_handle = vrep.simxGetObjectHandle(clientID,"ePuck_rightJoint", vrep.simx_opmode_blocking)

# Braitenberg weights for the 4 front prox sensors (avoidance):
braitFrontSens_leftMotor=[1,2,-2,-1] #these are sensors 2,3,4,5
# Braitenberg weights for the 2 side prox sensors 1 and 6 (following):
braitSideSens_leftMotor=[-1,0]
sensor_angles=[-math.pi/2.0,-math.pi/4.0,-math.pi/12.0,math.pi/12.0,math.pi/4.0, math.pi/2.0] #sensors at the front and sides. 0 for the rest


proximity_sensors=[]
sensor_vals=np.array([])
for i in range(1,6+1): #use only front facing sensors
    print("ePuck_proxSensor"+str(i))
    err_code,ps = vrep.simxGetObjectHandle(clientID,"ePuck_proxSensor"+str(i), vrep.simx_opmode_blocking)
    err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,ps,vrep.simx_opmode_streaming)    
    proximity_sensors.append(ps)
    sensor_vals=np.append(sensor_vals,np.linalg.norm(detectedPoint))

t = time.time() #record the initial time

while (time.time()-t)<30: #run for 20 seconds
    sensor_vals = np.array([])
    for i in range(1,6+1):
        err_code,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,proximity_sensors[i-1],vrep.simx_opmode_buffer)    
        sensor_vals = np.append(sensor_vals,np.linalg.norm(detectedPoint))
    # find the sensor that is closest to the target
    min_dist = np.where(sensor_vals==np.max(sensor_vals))
    min_dist = min_dist[0][0]
    
    print "Sensor vals",sensor_vals,"Min Dist:",min_dist,"Sensor vals min dis:",sensor_vals[min_dist]
    
    if sensor_vals[min_dist] < 0.2 and sensor_vals[min_dist]>0.00001 :
        steer = -1.0/sensor_angles[min_dist]
    else:
        steer = 0

    print ">","Steer:",steer
    vel=3
    kp=1
    vel_left = vel+kp*steer
    vel_right = vel-kp*steer
    
    err_code = vrep.simxSetJointTargetVelocity(clientID,l_motor_handle,vel_left,vrep.simx_opmode_streaming)
    err_code = vrep.simxSetJointTargetVelocity(clientID,r_motor_handle,vel_right,vrep.simx_opmode_streaming)
    #print (sensor_val,detectedPoint)
    #err_code,resolution,image = vrep.simxGetVisionSensorImage(clientID,camera,0,vrep.simx_opmode_buffer) 
    #img = np.array(image, dtype = np.uint8)
    #img.resize([resolution[0],resolution[1],3])
    #mlp.imshow(img,origin="lower")
    time.sleep(0.2)
     
vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
print("Done")