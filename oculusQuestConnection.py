import sys
import time
import openvr
import numpy

class oculusQuestConnection:
    def __init__(self):
        openvr.init(openvr.VRApplication_Scene)

    """
    #position, rotation, velocity, angular velocity
    # X left
    # Y Up
    # Z Forward
    """
    def getPosition(self):
        poses = []
        poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
        hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
        return hmd_pose.mDeviceToAbsoluteTracking

    def __del__(self):
        openvr.shutdown()