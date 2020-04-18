from serial.tools import list_ports

import dobot
import time

class dobotHandler:
    def __init__(self):
        port = list_ports.comports()[0].device
        print(port)
        device = dobot.Dobot(port=port, verbose=True)

        (x, y, z, r, j1, j2, j3, j4) = device.pose()
        print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')



        device.move_to(x, y+20, z, r, wait=False)
        device._set_queued_cmd_start_exec()
        time.sleep(1)
        (x, y, z, r, j1, j2, j3, j4) = device.pose()
        print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
        #device.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing

        device.close()

