import socket


class Client:
    def __init__(self):
        pass

    def listen(self):
        """
        Connect to a socket server and send a JSON with "connected" message.
        """

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('localhost', 65432))

        while True:
            data = conn.recv(1024)
            if not data:
                break

            self.process_message(data)

    def process_message(self, message):
        """
        Process a message from the server.
        """
        message = message.decode('utf-8')
        print(message)


def main():
    client = Client()
    client.listen()
