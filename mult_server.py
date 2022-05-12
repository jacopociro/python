#! /usr/bin/env python

import time
import zmq
import struct

def server(tcp):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    if tcp == 1:
        socket.bind("tcp://*:5555")
    elif tcp == 2:
        socket.bind("tcp://*:5556")
        

    while True:

        message = socket.recv()
        #print(message)
        values = struct.unpack('ddd', message)
        #print(values)

        time.sleep(1)

        socket.send("received!")
        return values

def main():
    vector = server(1)

    head = server(2)

    print("vector values:", vector)
    print("\n head values: ", head)

if __name__ == "__main__":
    main()