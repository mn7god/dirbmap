import socket
import os
import argparse
import requests
import subprocess


r = "\033[0;91m"
g = "\033[0;92m"
w = "\033[0;97m"
y = "\033[0;93m"

def port_scanner(domain):

    ip = socket.gethostbyname(domain)
    ports_opened = []
    
    for port in range(10, 9999):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.1)
        response = s.connect_ex((ip, port))
        
        if response == 0:
            ports_opened.append(port)
            print(f"{w}[{g}OPEN{w}] Port {y}{port}{w} is open on {y}{ip}{w} (domain: {y}{domain}{w})")
            interact_with_port(domain, ip, port)
        
        s.close() 
    
    print(f"{w}[{y}PORTS OPENED{w}] {ports_opened}") 

def interact_with_port(domain, ip, port):
    if port == 80 or port == 443:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has HTTP/HTTPS ports open. Enter website? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"xdg-open http://{domain}" if port == 80 else f"xdg-open https://{domain}")
    
    elif port == 21:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has FTP port open. Try FTP connection? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"ftp {ip}")

    elif port == 22:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has SSH port open. Try SSH connection? (y/n): ")
        if interaction.lower() == 'y':
            user = input("Do you want to use a username or brute force? (username/bruteforce): ")
            if user.lower() == 'username':
                username = input("Username: ")
                command = f"ssh {username}@{ip}"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"{w}[{r}ERROR]{w} Probably invalid user!")
                else:
                    print(f"{w}[{y}INFO{w}] Successfully connected!")
            elif user.lower() == 'bruteforce':
                with open("20pass.txt", 'r') as file:
                    for line in file.readlines():
                        line = line.strip()
                        print(f"{w}[{y}INFO{w}] Attempting BruteForce with user {y}{line}{w}")
                        command = f"ssh {line}@{ip}"
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            print(f"{w}[{g}SUCCESS{w}] Successful login with {y}{line}{w}!")
                            break
                        else:
                            print(f"{w}[{r}ERROR{w}] Invalid user!")
                print(f"{w}[{r}ERROR{w}] No valid users found!")

    elif port == 23:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has TELNET port open. Try telnet connection? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"telnet {ip}")

    elif port == 25:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has SMTP port open. Try SMTP connection? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"telnet {ip} 25")

    elif port == 110:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has POP3 port open. Try connect? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"telnet {ip} 110")

    elif port == 143 or port == 993:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has IMAP port open. Attempt connection? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"telnet {ip} {port}")

    elif port == 3306:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has MySQL port open. User or brute force? (user/brute): ")
        if interaction.lower() == 'user':
            username = input("Set a user: ")
            os.system(f"mysql -u {username} -h {ip} -p")
        elif interaction.lower() == 'brute':
            with open("mysql.txt", 'r') as file:
                for line in file.readlines():
                    line = line.strip()
                    print(f"{w}[{y}INFO{w}] Attempting brute force with user {y}{line}{w}...")
                    command = f"mysql -u {line} -h {ip} -p"
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{w}[{g}SUCCESS{w}] Successful login with {y}{line}{w}!")
                        break
                    else:
                        print(f"{w}[{r}ERROR{w}] Error: ", result.stderr)

    elif port == 5432:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has PostgreSQL port open. User or brute force? (user/brute): ")
        if interaction.lower() == 'user':
            username = input("Set a user: ")
            database = input("Set the name of the database you want to access: ")
            os.system(f"psql -U {username} -h {ip} -d {database}")
        elif interaction.lower() == 'brute':
            database = input("Set the name of the database you want to access: ")
            with open("mysql.txt", 'r') as file:
                for line in file.readlines():
                    line = line.strip()
                    print(f"{w}[{y}INFO{w}] Attempting brute force with user {y}{line}{w}...")
                    command = f"psql -U {line} -h {ip} -d {database}"
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{w}[{g}SUCCESS{w}] Successful login with {y}{line}{w}!")
                        break
                    else:
                        print(f"{w}[{r}ERROR{w}] Error: ", result.stderr)

    elif port == 3389:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has RDP port open. Try connection? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"xfreerdp /v:{ip}")

    elif port == 161:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has SNMP port open. Try connect? (y/n): ")
        if interaction.lower() == 'y':
            community_string = input("Community String: ")
            id = input("OID: ")
            command = f"snmpget -v 2c -c {community_string} {ip} {id}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{w}[{r}ERROR{w}] Error: ", result.stderr)

    elif port == 445:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has SMB port open. Try connect? (y/n): ")
        if interaction.lower() == 'y':
            community_string = input("Shared resource name: ")
            user = input("User: ")
            command = f"smbclient //{ip}/{community_string} -U {user}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"{w}[{r}ERROR{w}] Error: ", result.stderr)

    elif port == 5900:
        interaction = input(f"{w}[{y}INFO{w}] The domain {r}{domain}{w} has VNC port open. Try connect? (y/n): ")
        if interaction.lower() == 'y':
            os.system(f"vncviewer {ip}:5900")

    else:
        print(f"{w}[{y}INFO{w}] Port {port} is open but no specific interaction defined.")

def directory_search(domain):
    with open("dir.txt", 'r') as file:
        for line in file.readlines():
            req = requests.get(f"{domain}/{line.strip()}")
            if req.status_code == 200:
                print(f"{w}[{y}SUCCESS{w}] Directory Found: {domain}/{line.strip()}")

def main():
    parser = argparse.ArgumentParser(description="This is a simple program created in Python 3 to test websites...")
    parser.add_argument('operation', choices=['scan', 'dirs'], help="Please set an operation (scan/dirs)")
    parser.add_argument('url', type=str, help="Please provide a domain URL here")
    args = parser.parse_args()

    if args.operation == 'scan':
        port_scanner(args.url)
    elif args.operation == 'dirs':
        directory_search(args.url)

if __name__ == '__main__':
    main()

    
