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


def main(session):
    #ip_address = "192.168.1.100"
    ip_address = "130.251.13.143"
    port_num = 9559

    videoDevice = ALProxy('ALVideoDevice', ip_address, port_num)
    print(videoDevice)
    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1            # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = videoDevice.subscribeCamera("test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    print(captureDevice)
    # create image
    width = 320     
    height = 240
    image1 = np.zeros((height, width, 3), np.uint8)
    image2 = np.zeros((height, width, 3), np.uint8)
    while True:

        # get image
        result = videoDevice.getImageRemote(captureDevice);
        #print(result)
        if result == None:
            print ('cannot capture.')
        elif result[6] == None:
            print ('no image data string.')
        else:
            
            # translate value to mat
            values = map(ord, list(result[6]))
            i = 0
            for y1 in range(0, height):
                for x1 in range(0, width):
                    image1.itemset((y1, x1, 0), values[i + 0])
                    image1.itemset((y1, x1, 1), values[i + 1])
                    image1.itemset((y1, x1, 2), values[i + 2])
                    i += 3
            j = 0
            for y2 in range(0, height):
                for x2 in range(0, width):
                    image2.itemset((y2, x2, 0), values[j + 0])
                    image2.itemset((y2, x2, 1), values[j + 1])
                    image2.itemset((y2, x2, 2), values[j + 2])
                    j += 3
            # show image
            cv2.imshow("pepper-top-camera-320x240.1", image1)
            cv2.imshow("pepper-top-camera-320x240.2", image2)
        # exit by [ESC]
        if cv2.waitKey(33) == 27:
            videoDevice.unsubscribe("test") 
            break
    

    
#ip = "192.168.1.100"
ip = "130.251.13.143"

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