import socket


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created.")
    try:
        s.bind((host, port))
    except socket.error as e:
        if e == "[Errno 48] Address already in use":
            print("Already in use! Close and try again.")
            s.close()
    print("Socket bind complete.")
    return s


def setup_connection():
    s.listen(1) # Allows one connect at a time.
    conn, address = s.accept()
    print(f"Conected to: {address[0]}: {str(address[1])}")
    return conn


def GET():
    reply = data
    return reply


def REPEAT(data_message):
    reply = data_message[1]
    return reply


def data_transfer(conn):
    # A loop that sends/recieves data until halted.
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        # Split the data so that you have the command / data.
        data_message = data.split(" ", 1)
        command = data_message[0]
        if command == "GET":
            reply = GET()
        elif command == "REPEAT":
            reply = REPEAT(data_message)
        elif command == "EXIT":
            print("Client Disconnected.")
            break
        elif command == "KILL":
            print("Server Shutting Down...")
            s.close()
            break
        else:
            reply = "Unknown command. Please try again."
        # Send the reply back to the client.
        conn.sendall(str.encode(reply))
        print("Data has been sent to the client.")
    conn.close()

host = ""
port = 5560

s = start_server()

while True:
    conn = setup_connection()
    data_transfer(conn)
s.close()
