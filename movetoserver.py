#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use moveTo Method"""

import qi
import argparse
import sys
import time
import zmq
import struct


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.bind("tcp://*:5555")

        

    while True:

        message = socket.recv()
        #print(message)
        values = struct.unpack('ddd', message)
        #print(values)

        time.sleep(1)

        socket.send("received!")
        return values
    

def main(session):
## main con la fase di startup e calla movement per muoversi
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    motion_service.wakeUp()

    posture_service.goToPosture("StandInit", 0.5)
    try:
        while True:
            pos = server()
            x = pos[0]
            y = pos[1]
            theta = pos[2]
            print("reaching position %d %d %d",x, y, theta)
            motion_service.moveTo(x, y, theta)

            time.sleep(1)

            motion_service.stopMove()
    except KeyboardInterrupt:
            motion_service.rest()
            
##sistema per linkare a pepper

ip = "130.251.13.117"
#pepper 112
#nao 116

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