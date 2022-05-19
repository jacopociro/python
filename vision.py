#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Shows how images can be accessed through ALVideoDevice"""

import qi
import argparse
import sys
import time
import vision_definitions
import numpy as np
import cv2
from naoqi import ALProxy
import atexit

def exit_handler():
    global videoDevice, captureDevice
    a = videoDevice.releaseImage(captureDevice)
    b = videoDevice.unsubscribe(captureDevice) 
    if a & b:
        print("proper exit")
    


#ip = "192.168.1.100"
ip = "130.251.13.117"
def main(session):
    global ip
    global videoDevice, captureDevice
    #ip_address = "192.168.1.100"
    ip_address = ip
    port_num = 9559
    
    videoDevice = ALProxy('ALVideoDevice', ip_address, port_num)

    # subscribe top camera
    # 0 = topcamera ; 1 = botcamera; 2 = depthcamera; 3 = Stereocamera
    AL_kTopCamera = 0
    AL_kQVGA = 1           # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = videoDevice.subscribeCamera("test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 30)
    print(captureDevice)
    # create image
    width = 320 
    height = 240
    image = np.zeros((height, width, 3), np.uint8)
    while True:

        # get image
        result = videoDevice.getImageRemote(captureDevice);

        if result == None:
            print ('cannot capture.')
        elif result[6] == None:
            print ('no image data string.')
        else:

            # translate value to mat
            values = map(ord, list(result[6]))
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3

            # show image
            cv2.imshow("pepper-top-camera-320x240", image)
            atexit.register(exit_handler)
        # exit by [ESC]


    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=ip,
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)