#! /usr/bin/env python

import struct
import zmq
import math

def main():
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    a = input("pitch value...")
    b = input("yaw value...")
    a = math.radians(a)
    b = math.radians(b)
    c = 0
    
    
    var = struct.pack('ddd', a, b, c)
    #print(var)
    print("sending request...")
    socket.send(var)
        
    message = socket.recv()
    print(message)



if __name__ == "__main__":
    main()