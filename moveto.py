#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use moveToward Method"""

import qi
import argparse
import sys
import time

def movement():
## read speed from the keyboard
    x = float(input("set x:"))
    y = float(input("set y:"))
    theta = float(input("set theta:"))
    return x, y, theta


    

def main(session):
## main con la fase di startup e calla movement per muoversi
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    motion_service.wakeUp()

    posture_service.goToPosture("StandInit", 0.5)

    velocity = movement()
    x = velocity[0]
    y = velocity[1]
    theta = velocity[2]
    motion_service.moveTo(x, y, theta)

    time.sleep(1)

    motion_service.stopMove()
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