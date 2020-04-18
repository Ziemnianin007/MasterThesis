from serial.tools import list_ports

import dobot
import time

#joint1 min -125 max 125
#joint 2 min -5 max 90
#j3 min - 15 max 90
#joint4 min -150 max 150

class dobotHandler:
    def __init__(self):
        port = list_ports.comports()[0].device
        print(port)
        device = dobot.Dobot(port=port, verbose=True)

        (x, y, z, r, j1, j2, j3, j4) = device.pose()
        print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')



        device.speed()
        device.move_to(x, y, z+20, r+100, wait=True)
        device._set_queued_cmd_start_exec()
        time.sleep(1)
        (x, y, z, r, j1, j2, j3, j4) = device.pose()
        print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        #device.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing

        device.close()

