#! /usr/bin/env python

import time
import zmq
import struct

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:

        message = socket.recv()
        #print(message)
        values = struct.unpack('ddd', message)
        print(values)

        time.sleep(1)

        socket.send("received!")

if __name__ == "__main__":
    main()

        