#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Shows how images can be accessed through ALVideoDevice"""

import qi
import argparse
import sys
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
    #exit handler
    atexit.register(exit_handler)
    #videoDevice = ALProxy('ALVideoDevice', ip_address, port_num)
    videoDevice = session.service("ALVideoDevice")
    # subscribe camera
    # 0 = topcamera ; 1 = botcamera; 2 = depthcamera
    # color space 13 or 11 for depthcamera
    camera_idx = 2
    resolution = 1           # 320x240
    color_space = 11
    captureDevice = videoDevice.subscribeCamera("test", camera_idx, resolution, color_space, 30)
    
    if captureDevice:
        print ("[INFO] Camera is initialized")
    else:
        print("[INFO] Camera is not initialized")
        videoDevice.unsubscribe(captureDevice) 
    while True:
        image_raw = videoDevice.getImageRemote(captureDevice)
        if image_raw == None:
            print ('cannot capture.')
            videoDevice.releaseImage(captureDevice)
            break
        elif image_raw[6] == None:
            print ('no image data string.')
            videoDevice.releaseImage(captureDevice)
            break
        else:
        #print(image_raw)
            image = np.frombuffer(image_raw[6], np.uint8).reshape(image_raw[1], image_raw[0], 3)
            cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Camera", 1080, 1080)
            cv2.imshow("Camera", image)
            
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