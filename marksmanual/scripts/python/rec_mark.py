import socket

host = "192.168.1.191"
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    command = input("Enter your command: ")
    if command == "EXIT":
        # Send EXIT request to other end
        s.send(str.encode(command))
        break
    elif command == "KILL"
        # Send KILL command
        s.send(str.encode(command))
        print("KILLING SERVER")
        break
    s.send(str.encode(command))
    reply = s.recv(1024)
    print(reply.decode('utf-8'))

s.close()
