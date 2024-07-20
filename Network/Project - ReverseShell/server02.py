import socket
import sys

import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]

queue = Queue()
all_connections = []
all_address = []

# create a socket ( connect to computers )
def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9999

        s = socket.socket()
    
    except socket.error as msg:
        print("socket creation error: " + str(msg))

# binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port "+str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" +str(msg)+"Retrying...")
        bind_socket()
