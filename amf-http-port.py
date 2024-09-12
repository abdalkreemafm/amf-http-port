import socket
import sys
from time import sleep
from datetime import datetime
import threading
import psutil

def scan_port(ip, port, proto):
    try:
        if proto == "tcp":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif proto == "udp":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.05)
        if s.connect_ex((ip, port)) == 0:
            try:
                serv = socket.getservbyport(port, proto)
            except socket.error:
                serv = "Unknown Service"
            process = psutil.Process(s.getsockname()[1])
            print("Port %s Open Service:%s Protocol:%s Process:%s" % (port, serv, proto, process.name()))
        s.close()
    except Exception as e:
        pass

def main():
    ip = input("===>Abonsr!! ENTER YOUR IP TO START: ")
    t1 = datetime.now()
    print("Scanning Start.. %s Please Wait.. " % ip)
    sleep(1)

    threads = []
    for port in range(1, 65536):
        thread = threading.Thread(target=scan_port, args=(ip, port, "tcp"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    threads = []
    for port in range(1, 65536):
        thread = threading.Thread(target=scan_port, args=(ip, port, "udp"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    t2 = datetime.now()
    t3 = t2 - t1
    print("Scanning Completed On %s" % t3)

    while True:
        print("Do you want to scan for specific ports or protocols? (y/n)")
        choice = input()
        if choice == "y":
            while True:
                print("What do you want to scan? (p: ports, pr: protocols)")
                scan_choice = input()
                if scan_choice == "p":
                    while True:
                        try:
                            start_port = int(input("Enter the starting port number: "))
                            end_port = int(input("Enter the ending port number: "))
                            if start_port <= end_port:
                                break
                            else:
                                print("Invalid port range. Starting port must be less than or equal to ending port.")
                        except ValueError:
                            print("Invalid input. Please enter numbers only.")
                    print("What protocol do you want to scan? (tcp/udp)")
                    proto = input()
                    while proto.lower() not in ["tcp", "udp"]:
                        print("Invalid protocol. Please enter 'tcp' or 'udp'.")
                        proto = input()
                    t1 = datetime.now()
                    print("Scanning Start.. %s Please Wait.. " % ip)
                    sleep(1)
                    threads = []
                    for port in range(start_port, end_port + 1):
                        thread = threading.Thread(target=scan_port, args=(ip, port, proto.lower()))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()
                    t2 = datetime.now()
                    t3 = t2 - t1
                    print("Scanning Completed On %s" % t3)
                elif scan_choice == "pr":
                    print("What protocol do you want to scan? (tcp/udp)")
                    proto = input()
                    while proto.lower() not in ["tcp", "udp"]:
                        print("Invalid protocol. Please enter 'tcp' or 'udp'.")
                        proto = input()
                    t1 = datetime.now()
                    print("Scanning Start.. %s Please Wait.. " % ip)
                    sleep(1)
                    threads = []
                    for port in range(1, 65536):
                        thread = threading.Thread(target=scan_port, args=(ip, port, proto.lower()))
                        threads.append(thread)
                        thread.start()
                    for thread in threads:
                        thread.join()
                    t2 = datetime.now()
                    t3 = t2 - t1
                    print("Scanning Completed On %s" % t3)
                else:
                    print("Invalid choice. Please enter 'p' or 'pr'.")
        else:
            break

if __name__ == "__main__":
    main()
