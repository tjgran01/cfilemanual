import socket

class MarkServer(object):

    def __init__(self):
        self.host = ""
        self.port = 5560
        self.server = self.start_server()

        while True:
            self.conn = self.setup_connection()
            if self.conn:
                break

        print("We have a connection!")

    def setup_connection(self):
        self.server.listen(1) # Allows one connection at a time.
        conn, address = self.server.accept()
        print(f"Conected to: {address[0]}: {str(address[1])}")
        return conn


    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created.")
        try:
            s.bind((self.host, self.port))
        except socket.error as e:
            if e == "[Errno 48] Address already in use":
                print("Already in use! Close and try again.")
                s.close()
        print("Socket bind complete.")
        return s


    def data_transfer(self, data):
        try:
            data = str(data)
        except TypeError as e:
            print("Data provided cannot be converted to a string.")
            return None
        self.conn.sendall(str.encode(data))
        print("Data has been sent to the client.")


    def close_connection(self):
        self.conn.close()
