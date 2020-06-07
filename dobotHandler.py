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
    def __init__(self, emulation = False):
        self.emulation = emulation
        if(self.emulation is False):
            port = list_ports.comports()[0].device
            print(port)
            self.device = dobot.Dobot(port=port, verbose=False)
            self.device.speed()
        else:
            self.device = None
            self.pastStep = 30
            self.xList = [259.1198]
            self.yList = [0]
            self.zList = [-8.5687]
        self.position = None #(x, y, z, r, j1, j2, j3, j4)
        self.getTime = None


    def registeredPosition(self):
        return self.position

    def getPosition(self):
        if(self.emulation is True):
            if(len(self.zList) <= self.pastStep+1):
                position = []
                position.append(self.xList[0])
                position.append(self.yList[0])
                position.append(self.zList[0])
                self.position = position
                return position
            else:
                position = []
                position.append(self.xList[-self.pastStep])
                position.append(self.yList[-self.pastStep])
                position.append(self.zList[-self.pastStep])
                self.position = position
                return position

        self.position = self.device.pose()
        #print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        return self.position

    def getPositionTimeStamp(self):
        beforeTime = time.time()
        self.position = self.getPosition()
        afterTime = time.time()
        self.getTime = (afterTime + beforeTime)/2
        #print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        return self.position, self.getTime

    def setPosition(self, x = 259.1198, y = 0, z=-8.5687, r=0 ,wait = False, joint=False):
        positionTimeStamp = self.getPositionTimeStamp()
        #self.getPosition()
        if(self.emulation is True):
            if joint is False:
                self.xList.append(x)
                self.yList.append(y)
                self.zList.append(z)
            else:
                self.xList = [259.1198]
                self.yList = [0]
                self.zList = [-8.5687]
            return positionTimeStamp

        self.device._set_queued_cmd_clear()
        if joint is False:
            self.device.move_to(x, y, z, r, wait)
        else:
            self.device.move_to_joint(x, y, z, r, wait)
        return positionTimeStamp
        #self.device.go(x, y, z, r, wait)
        #self.device._set_queued_cmd_start_exec()


    def closerToPosition(self, x = 259.1198, y = 0, z=-8.5687, maxMove = 30, r=0 ,wait = False):
        self.device._set_queued_cmd_clear()
        positionWithTimeStamp = self.getPositionTimeStamp()
        (xTo, yTo, zTo, r, j1, j2, j3, j4) = self.position

        maxMoveX = maxMove
        maxMoveY = maxMove
        maxMoveZ = maxMove

        xCloser = x
        yCloser = y
        zCloser = z

        if x > xTo   + maxMoveX: xCloser = xTo   + maxMoveX
        if x < xTo   - maxMoveX: xCloser = xTo   -maxMoveX

        if y >  yTo  +maxMoveY: yCloser = yTo   +maxMoveY
        if y <  yTo  -maxMoveY: yCloser = yTo   -maxMoveY

        if z > zTo   +maxMoveZ: zCloser = zTo   +maxMoveZ
        if z < zTo   -maxMoveZ: zCloser = zTo   -maxMoveZ
        #print("X: %0.3f " % xCloser, "Y: %0.3f " % yCloser, "Z: %0.3f " % zCloser)
        self.device.move_to(xCloser, yCloser, zCloser, r, wait)
        return positionWithTimeStamp

    def __del__(self):
        self.device.close()
