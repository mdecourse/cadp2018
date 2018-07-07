import vrep
import sys
# child threaded script: 
# 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
#simExtRemoteApiStart(19999)
 
vrep.simxFinish(-1)
 
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
 
if clientID!= -1:
    print("Connected to remote server")
else:
    print('Connection not successful')
    sys.exit('Could not connect')
 
errorCode,Revolute_joint_handle=vrep.simxGetObjectHandle(clientID,'Revolute_joint',vrep.simx_opmode_oneshot_wait)
 
if errorCode == -1:
    print('Can not find left or right motor')
    sys.exit()
 
errorCode=vrep.simxSetJointTargetVelocity(clientID,Revolute_joint_handle,2, vrep.simx_opmode_oneshot_wait)

while True:
    choice = input("(e to exit, p to pause and enter to exec)>")
    if choice == "e":
        print("exiting")
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)
        break
    elif choice == "p":
        vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    else:
        vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)