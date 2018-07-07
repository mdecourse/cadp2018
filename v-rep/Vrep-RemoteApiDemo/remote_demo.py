##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import vrep

##==============================================================#
## SECTION: Class Definitions                                   #
##==============================================================#

class Robot:
    def __init__(self, client_id, opmode):
        self.cid = client_id
        self.op = opmode

        # Setup wheel joints.
        self.wj_locs = ["Left","Right"]
        self.wjs = {}
        for loc in self.wj_locs:
            name = "Dynamic{0}Joint".format(loc)
            _,h = vrep.simxGetObjectHandle(client_id, name, opmode)
            self.wjs[loc] = h

        # Setup vision sensors.
        self.vs_locs = ["Left","Middle","Right"]
        self.vss = {}
        for loc in self.vs_locs:
            name = "{0}Sensor".format(loc)
            _,h = vrep.simxGetObjectHandle(client_id, name, opmode)
            self.vss[loc] = h

    def set_wheel_vel(self, left, right):
        """Sets the wheel target velocities."""
        vrep.simxSetJointTargetVelocity(self.cid, self.wjs['Left'], left, self.op)
        vrep.simxSetJointTargetVelocity(self.cid, self.wjs['Right'], right, self.op)

    def get_wheel_vel(self):
        """Returns the wheel velocities as a list of (left,right)."""
        vels = []
        for loc in self.wj_locs:
            _,vel = vrep.simxGetObjectFloatParameter(self.cid, self.wjs[loc], vrep.sim_jointfloatparam_velocity, self.op)
            vels.append(vel)
        return vels

    def get_vis_sensors(self):
        """Returns a list of lists containing the average red/green/blue value
        from the left/middle/right vision sensor."""
        aves = []
        for loc in self.vs_locs:
            h = self.vss[loc]
            _,_,pkt = vrep.simxReadVisionSensor(client_id, h, opmode)
            aves.append(pkt[0][11:14])
        return aves

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

def is_green(a):
    """Returns true if the reading from Robot.get_vis_sensors() is green."""
    return (a[0] < 0.4 and a[2] < 0.4) and (a[1] > 0.5)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    vrep.simxFinish(-1) # Stop any running simulation.
    client_id = vrep.simxStart("127.0.0.1", 19997, True, True, 5000, 5)
    if client_id == -1:
        print("Failed to connect.")
        exit()
    print("Connected to V-REP.")
    print("Running robot logic, will exit when simulation is ended...")
    try:
        opmode = vrep.simx_opmode_blocking
        vrep.simxStartSimulation(client_id, opmode)
        robot = Robot(client_id, opmode)
        speed = 2
        robot.set_wheel_vel(1.0*speed, 1.0*speed)
        vrep.simxSynchronousTrigger(client_id)
        while True:
            # Very simple robot line following logic.
            l,m,r = robot.get_vis_sensors()
            if is_green(m):
                robot.set_wheel_vel(1.0*speed, 1.0*speed)
            elif is_green(l):
                robot.set_wheel_vel(0.2*speed, 1.0*speed)
            elif is_green(r):
                robot.set_wheel_vel(1.0*speed, 0.2*speed)
            vrep.simxSynchronousTrigger(client_id)
    except:
        vrep.simxFinish(client_id)
        print("Simulation ended.")
