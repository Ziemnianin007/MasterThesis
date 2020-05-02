from serial.tools import list_ports

import dobot
import time

#joint1 min -125 max 125
#joint 2 min -5 max 90
#j3 min - 15 max 90
#joint4 min -150 max 150
#Initial
#x 259,1198
#y 0
#z -8.5687
#R 0
#Min/Max
#x Min -135  Max 328    av 96.5     +- 231.5
#y Min -328 Max 328     av 0        +- 328
#z Min -30 Max 160      av 65       +- 95
#R Min -150 Max 150     av 0        +- 150

class dobotHandler:
    device = None
    def __init__(self):
        port = list_ports.comports()[0].device
        print(port)
        self.device = dobot.Dobot(port=port, verbose=False)
        self.device.speed()

    def getPosition(self):
        (x, y, z, r, j1, j2, j3, j4) = self.device.pose()
        #print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        return (x, y, z, r, j1, j2, j3, j4)

    def setPosition(self, x = 259.1198, y = 0, z=-8.5687, r=0 ,wait = False):
        self.device._set_queued_cmd_clear()
        self.device.move_to(x, y, z, r, wait)
        #self.device.go(x, y, z, r, wait)
        #self.device._set_queued_cmd_start_exec()


    def closerToPosition(self, x = 259.1198, y = 0, z=-8.5687, r=0 ,wait = False):
        self.device.speed()
        (xTo, yTo, zTo, r, j1, j2, j3, j4) = self.device.pose()

        maxMoveX = 30
        maxMoveY = 30
        maxMoveZ = 30

        xCloser = x - xTo
        yCloser = y - yTo
        zCloser = z - zTo

        if xCloser > xTo   +maxMoveX: xCloser = xTo   +maxMoveX
        if xCloser < xTo   -maxMoveX: xCloser = xTo   -maxMoveX

        if yCloser >  yTo  +maxMoveY: yCloser = yTo   +maxMoveY
        if yCloser <  yTo  -maxMoveY: yCloser = yTo   -maxMoveY

        if zCloser > zTo   +maxMoveZ: zCloser = zTo   +maxMoveZ
        if zCloser < zTo   -maxMoveZ: zCloser = zTo   -maxMoveZ
        print("X: %0.3f " % xCloser, "Y: %0.3f " % yCloser, "Z: %0.3f " % zCloser)
        self.device.move_to(xCloser, yCloser, zCloser, r, wait)
        self.device._set_queued_cmd_start_exec()

    def __del__(self):
        self.device.close()
