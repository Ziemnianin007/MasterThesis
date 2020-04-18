import sys
import time
import openvr
import numpy

class oculusQuestConnection:
    def __init__(self):
        openvr.init(openvr.VRApplication_Scene)
        poses = []  # will be populated with proper type after first call
        for i in range(10):
            poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
            hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
            #position, rotation, velocity, angular velocity
            # X left
            # Y Up
            # Z Forward
            print(hmd_pose.mDeviceToAbsoluteTracking)
            sys.stdout.flush()
            time.sleep(0.2)
        openvr.shutdown()
