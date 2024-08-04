import socket
import os
import gc
import sys
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
import platform

HOST = '127.0.0.1'
START_PORT = 1
END_PORT = 1024
max_workers = 100

open_ports_file = 'open_ports.txt'
total_ports = END_PORT - START_PORT + 1
scanned_ports = 0

class ProgressMsg:
    def __init__(self):
        self.scanned_ports = 0
        self.total_ports = 0
        self.elapsed_time = 0
        self.progress_msg = ''

    def generate_progress_msg(self):
        progress_percent = (self.scanned_ports / self.total_ports) * 100
        bar_length = 40
        filled_length = int(bar_length * self.scanned_ports / self.total_ports)
        empty_length = bar_length - filled_length

        filled_color = '\033[91m'     # Light Red
        empty_color = '\033[90m'      # Dark Gray
        reset_color = '\033[0m'       # Reset

        bar = filled_color + '█' * filled_length + empty_color + '█' * empty_length + reset_color

        self.progress_msg = f"""\

Scanned ports:       {self.scanned_ports}
Total ports:         {self.total_ports}
Elapsed time:        {self.elapsed_time:.2f} seconds

{bar} {progress_percent:.2f}%

"""

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((HOST, port))
        return port, True
    except:
        return port, False
    finally:
        s.close()

def scan_ports(start_port, end_port, max_workers):
    global scanned_ports

    progress = ProgressMsg()
    progress.total_ports = end_port - start_port + 1

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, port): port for port in range(start_port, end_port + 1)}
        open_ports = []

        for future in futures:
            port, is_open = future.result()
            scanned_ports += 1
            if is_open:
                open_ports.append(port)
                with open(open_ports_file, 'a') as f:
                    f.write(f"{port}\n")

            if scanned_ports % 10 == 0:
                progress.scanned_ports = scanned_ports
                progress.elapsed_time = time.time() - start_time
                progress.generate_progress_msg()
                sys.stdout.write('\033[F\033[K' * 7)
                sys.stdout.write(progress.progress_msg)
                sys.stdout.flush()

    progress.scanned_ports = scanned_ports
    progress.elapsed_time = time.time() - start_time
    progress.generate_progress_msg()
    sys.stdout.write('\033[F\033[K' * 7)
    sys.stdout.write(progress.progress_msg)
    sys.stdout.flush()

    return open_ports

def launch_open_ports_display():
    os_name = platform.system()
    if os_name == 'Linux':
        terminal_command = ['gnome-terminal', '--', 'python3', '-c', 'import port_scanner; port_scanner.display_open_ports()']
    elif os_name == 'Darwin':  # macOS
        terminal_command = ['open', '-a', 'Terminal', 'python3', '-c', 'import port_scanner; port_scanner.display_open_ports()']
    elif os_name == 'Windows':
        terminal_command = ['cmd', '/c', 'start', 'python', '-c', 'import port_scanner; port_scanner.display_open_ports()']
    else:
        raise Exception(f"Unsupported operating system: {os_name}")

    subprocess.Popen(terminal_command)

def display_open_ports():
    with open(open_ports_file, 'r') as f:
        ports = f.read().strip().split('\n')
        ports = [port for port in ports if port]  # Filter out empty lines
    if ports:
        print("Open Ports:\n" + '\n'.join(ports))
    else:
        print("No open ports found.")

if __name__ == "__main__":
    # Clear the open_ports_file at the start
    with open(open_ports_file, 'w'):
        pass
    launch_open_ports_display()
    open_ports = scan_ports(START_PORT, END_PORT, max_workers)
    display_open_ports()
