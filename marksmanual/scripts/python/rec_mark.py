import socket
import serial
import sys

def get_host_ip():
    try:
        with open("server_ip.txt") as in_file:
            host = in_file.read()
            return host
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


host = get_host_ip()
if not host:
    print("No Server IP found. Closing program.")
    sys.exit()
print(host)
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def get_mark():
    while True:
        reply = s.recv(1024)
        print(reply.decode("utf-8"))
        if reply.decode("utf-8") == "KILL":
            s.close()
            sys.exit()
        else:
            print("Do something fancy")
            send_to_fnirs(reply)

while True:
    print("Waiting for reply.. ..")
    reply = get_mark()

s.close()
