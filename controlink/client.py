import socket


class Client:
    def __init__(self, host, port=65432):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("Connection closed by server.")
                    break
                print('Mouse position:', data.decode('utf-8'))


def main():
    server_ip = '127.0.0.1'
    client = Client(server_ip)
    client.run()


if __name__ == "__main__":
    main()
