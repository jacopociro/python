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
import atexit

    
#ip = "192.168.1.100"
ip = "130.251.13.117"
def exit_handler():
    global videoDevice, captureDevice
    a = videoDevice.releaseImage(captureDevice)
    b = videoDevice.unsubscribe(captureDevice) 
    if a & b:
        print("proper exit")
        

def main(session):
    global ip, videoDevice, captureDevice
    #ip_address = "192.168.1.100"
    ip_address = ip
    port_num = 9559

    videoDevice = session.service("ALVideoDevice")
    atexit.register(exit_handler)
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
        image_raw = videoDevice.getImageRemote(captureDevice);
        #print(image_raw)
        if image_raw == None:
            print ('cannot capture.')
        elif image_raw[6] == None:
            print ('no image data string.')
        else:
            image = np.frombuffer(image_raw[6], np.uint8).reshape(image_raw[1], image_raw[0], 3)
            cv2.namedWindow("Camera1", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Camera1", 540, 540)
            cv2.namedWindow("Camera2", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Camera2", 540, 540)
            # show image
            cv2.imshow("Camera1", image)
            cv2.imshow("Camera2", image)
        # exit by [ESC]
        if cv2.waitKey(33) == 27: 
            break
    



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