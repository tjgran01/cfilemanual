import socket
import serial
import sys
import csv

def get_host_ip():
    try:
        with open("server_ip.txt") as in_file:
            host = in_file.read()
            return host
    except FileNotFoundError:
        return None


def get_host_ips():
    try:
        with open("server_ip.csv", "r") as in_csv:
            ips = csv.reader(in_csv, delimiter=",")
            hosts = [ip for ip in ips]
            return hosts
    except FileNotFoundError:
        return None


def send_to_fnirs(data):
    port = serial.Serial("/dev/ttyUSB0",
                         baudrate=9600,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS,
                         writeTimeout = 0,
                         timeout = 10)
    print(port.isOpen())
    port.write(data)
    port.close()
    print(port.isOpen())


def get_mark():
    while True:
        reply = s.recv(1024)
        print(reply.decode("utf-8"))
        if reply.decode("utf-8") == "KILL":
            s.close()
            sys.exit()
        else:
            send_to_fnirs(reply)


hosts = get_host_ips()
if not hosts:
    print("File 'server_ip.csv' not found. Closing program.")
    sys.exit()
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for host in hosts:
    print(host)
    host = str(host)[2:-2]
    print(host)
    try:
        s.connect((host, port))
        break
    except:
        print("could not connect")
        continue

while True:
    print("Waiting for mark.. ..")
    reply = get_mark()

s.close()
