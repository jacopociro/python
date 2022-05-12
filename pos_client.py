#! /usr/bin/env python

import struct
import zmq
import math

def main():
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    a = input("x value...")
    b = input("y value...")
    c = input("theta value in degrees...")
    c = math.radians(c)
    
    
    var = struct.pack('ddd', a, b, c)
    #print(var)
    print("sending request...")
    socket.send(var)
        
    message = socket.recv()
    print(message)



if __name__ == "__main__":
    main()