import sockets
import sys

# create a socket ( connect to computers )
def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9999
    
    except socket.error as msg:
        print("socket creation error: " + str(msg))