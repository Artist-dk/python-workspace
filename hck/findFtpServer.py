import psutil

def get_ftp_servers():
    ftp_servers = []
    connections = psutil.net_connections(kind='tcp')
    
    for conn in connections:
        if conn.status == psutil.CONN_ESTABLISHED and conn.laddr.port == 21:
            remote_ip = conn.raddr.ip
            if remote_ip not in ftp_servers:
                ftp_servers.append(remote_ip)
    
    return ftp_servers

if __name__ == "__main__":
    ftp_servers = get_ftp_servers()
    
    if ftp_servers:
        print("FTP Servers Connected to Your Computer:")
        for server in ftp_servers:
            print(server)
    else:
        print("No FTP servers found.")
