import dobotHandler
import oculusQuestConnection
#home dobot magician in dobotstudio, then disconnect and run
dobotHandlerInstance = dobotHandler.dobotHandler()


oculusQuestConnectionInstance = oculusQuestConnection.oculusQuestConnection()

#x Min -135  Max 328    av 96.5     +- 231.5
#y Min -328 Max 328     av 0        +- 328
#z Min -30 Max 160      av 65       +- 95
#R Min -150 Max 150     av 0        +- 150

"""
#position, rotation, velocity, angular velocity
# X left
# Y Up
# Z Forward
"""
homeX = None
homeY = None
homeZ = None
homePosition = oculusQuestConnectionInstance.getPosition()
def homePositionF():
    homePosition = oculusQuestConnectionInstance.getPosition()
    homeX = homePosition[0][3]
    homeY = homePosition[2][3]
    homeZ = homePosition[1][3]
def relativeHome(x,y,z):
    homePosition[0][3] = homePosition[0][3] - (x - oldPosition[0]) #+- 0.25
    homePosition[2][3] = homePosition[2][3] - (y - oldPosition[1]) #+= 0.25
    homePosition[1][3] = homePosition[1][3] - (z - oldPosition[2]) # +0.5 -0.1
grip = False
dobotHandlerInstance.setPosition(259.1198, 0, 8.5687)
oldPosition = [homePosition[0][3], homePosition[2][3], homePosition[1][3]]
while(1):
    position = oculusQuestConnectionInstance.getPosition()
    oldGrip = grip
    grip = oculusQuestConnectionInstance.getRightControllerGrip()
    x = position[0][3] - homePosition[0][3] #+- 0.25
    y = position[2][3] - homePosition[2][3] #+= 0.25
    z = position[1][3] - homePosition[1][3] # +0.5 -0.1
    if grip is not oldGrip and grip is True:
        #relativeHome(x,y,z)
        pass
    print("X: %0.3f " % x, "Y: %0.3f " % y, "Z: %0.3f " % z, " grip: ", grip)
    if grip is True:
        oldPosition = [x,y,z]
        oculusQuestConnectionInstance.resetZero()
        xDobot = -y / 0.25 * 231.5 + 259.1198
        yDobot = -x / 0.25 * 328 + 0
        zDobot = z / 0.25 * 150 + 0 - 8.5687
        if zDobot < -30:
            zDobot = -30
        dobotHandlerInstance.setPosition(xDobot, yDobot, zDobot)



    #print("X: %0.3f " % xDobot, "Y: %0.3f " % yDobot, "Z: %0.3f " % zDobot)

    #print(position)

    # x = position[0][0] - homePosition[0][0]
    # y = position[0][1] - homePosition[0][1]
    # z = position[0][2] - homePosition[0][2]
    # a = position[0][3] - homePosition[0][3]
    #
    # x1 = position[1][0] - homePosition[1][0]
    # y1 = position[1][1] - homePosition[1][1]
    # z1 = position[1][2] - homePosition[1][2]
    # a1 = position[1][3] - homePosition[1][3]
    #
    # x2 = position[2][0] - homePosition[2][0]
    # y2 = position[2][1] - homePosition[2][1]
    # z2 = position[2][2] - homePosition[2][2]
    # a2 = position[2][3] - homePosition[2][3]
    # print("X: %0.3f " % x,"Y: %0.3f " % y,"Z: %0.3f " % z,"A: %0.3f " % a, "X: %0.3f " % x1,"Y: %0.3f " % y1,"Z: %0.3f " % z1,"A: %0.3f " % a1 , "X: %0.3f " % x2,"Y: %0.3f " % y2,"Z: %0.3f " % z2,"A: %0.3f " % a2)

    # #print(x,y,z)
    #dobotHandlerInstance.setPosition(x,y,z)