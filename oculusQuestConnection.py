import sys
import time
import openvr
import numpy
import pprint

class oculusQuestConnection:
    def __init__(self, emulateOculus = True, emulationData = None):

        if emulateOculus is False:
            openvr.init(openvr.VRApplication_Scene)
            self.VRSystem = openvr.VRSystem()
            self.VRSystem.resetSeatedZeroPose()
            self.VRCompositor = openvr.VRCompositor()
        #else:
        self.emulateOculus = emulateOculus
        self.emulationData = emulationData
        self.emulationDataIndex = 0
        self.emulationGrip = True

    """
    #position, rotation, velocity, angular velocity
    # X left
    # Y Up
    # Z Forward
    """

    def loadData(self, emulationData = None):
        self.emulateOculus = True
        self.emulationGrip = True
        self.emulationData = emulationData
        self.emulationDataIndex = 0

    def from_controller_state_to_dict(self, pControllerState):
        # docs: https://github.com/ValveSoftware/openvr/wiki/IVRSystem::GetControllerState
        d = {}
        d['unPacketNum'] = pControllerState.unPacketNum
        # on trigger .y is always 0.0 says the docs
        d['trigger'] = pControllerState.rAxis[1].x
        # 0.0 on trigger is fully released
        # -1.0 to 1.0 on joystick and trackpads
        d['trackpad_x'] = pControllerState.rAxis[0].x
        d['trackpad_y'] = pControllerState.rAxis[0].y
        # These are published and always 0.0
        # for i in range(2, 5):
        #     d['unknowns_' + str(i) + '_x'] = pControllerState.rAxis[i].x
        #     d['unknowns_' + str(i) + '_y'] = pControllerState.rAxis[i].y
        d['ulButtonPressed'] = pControllerState.ulButtonPressed
        d['ulButtonTouched'] = pControllerState.ulButtonTouched
        # To make easier to understand what is going on
        # Second bit marks menu button
        d['menu_button'] = bool(pControllerState.ulButtonPressed >> 1 & 1)
        # 32 bit marks trackpad
        d['trackpad_pressed'] = bool(pControllerState.ulButtonPressed >> 32 & 1)
        d['trackpad_touched'] = bool(pControllerState.ulButtonTouched >> 32 & 1)
        # third bit marks grip button
        d['grip_button'] = bool(pControllerState.ulButtonPressed >> 2 & 1)
        # System button can't be read, if you press it
        # the controllers stop reporting
        return d

    def getPosition(self):
        if(self.emulateOculus is True):
            if len(self.emulationData['oculusX']) <= self.emulationDataIndex:
                self.emulationDataIndex = len(self.emulationData['oculusX']) - 1
                self.emulationGrip = False
            position = []
            position.append([])
            position.append([])
            position.append([])
            position[0].append(0)
            position[0].append(0)
            position[0].append(0)
            position[0].append(0)
            position[1].append(0)
            position[1].append(0)
            position[1].append(0)
            position[1].append(0)
            position[2].append(0)
            position[2].append(0)
            position[2].append(0)
            position[2].append(0)
            position[2][3] = (self.emulationData['oculusX'][self.emulationDataIndex] - 259.1198) /1000
            position[0][3] = -(self.emulationData['oculusY'][self.emulationDataIndex]) /1000
            position[1][3] = (self.emulationData['oculusZ'][self.emulationDataIndex] + 8.5687) /1000
            self.emulationDataIndex += 1
            # self.oculusX = position[2][3] * 1000 + 259.1198
            # self.oculusY = -position[0][3] * 1000 + 0
            # self.oculusZ = position[1][3] * 1000 + 0 - 8.5687
            # self.positionArray['oculusX'].append(self.oculusX)
            # self.positionArray['oculusY'].append(self.oculusY)
            # self.positionArray['oculusZ'].append(self.oculusZ)
            # self.positionArray['oculusTimeStamp'].append(time.time())
            # self.emulationData
            # self.rightX = position[0][3] - self.homeX  # +- 0.25
            # self.rightY = position[2][3] - self.homeY  # += 0.25
            # self.rightZ = position[1][3] - self.homeZ  # +0.5 -0.1
            return position
        else:
            poses = []
            poses, _ = self.VRCompositor.waitGetPoses(poses, None)
            """
            k_unTrackedDeviceIndex_Hmd
        {"name": "TrackedControllerRole_Invalid","value": "0"}
        ,{"name": "TrackedControllerRole_LeftHand","value": "1"}
        ,{"name": "TrackedControllerRole_RightHand","value": "2"}
            """
            hmd_pose = poses[openvr.TrackedControllerRole_RightHand]
            return hmd_pose.mDeviceToAbsoluteTracking

    def controllerState(self, controllerId = openvr.TrackedControllerRole_RightHand):
        result, pControllerState = self.VRSystem.getControllerState(controllerId)
        d = self.from_controller_state_to_dict(pControllerState)
        #pprint.pprint(d)
        return d

    def getRightControllerTrigger(self):
        return self.controllerState()['trigger']

    def getRightControllerGrip(self):
        if (self.emulateOculus is True):
            return self.emulationGrip
        else:
            return self.controllerState()['grip_button']

    def resetZero(self):
        if(self.emulateOculus is False):
            self.VRSystem.resetSeatedZeroPose()

    def __del__(self):
        if(self.emulateOculus is False):
            openvr.shutdown()