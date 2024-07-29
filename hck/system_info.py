import os
import platform
import psutil
import socket

def get_system_info():
    # Basic Information
    info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "Disk Size": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
        "Disk Free": f"{psutil.disk_usage('/').free / (1024 ** 3):.2f} GB",
        "Disk Used": f"{psutil.disk_usage('/').used / (1024 ** 3):.2f} GB",
        "Network Interfaces": get_network_interfaces()
    }

    return info

def get_network_interfaces():
    interfaces = {}
    for interface, addrs in psutil.net_if_addrs().items():
        interface_info = []
        for addr in addrs:
            interface_info.append(f"{addr.family.name}: {addr.address}")
        interfaces[interface] = ", ".join(interface_info)
    return interfaces

def print_system_info(info):
    print("System Information")
    print("===================")
    for key, value in info.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print("===================")

if __name__ == "__main__":
    system_info = get_system_info()
    print_system_info(system_info)
