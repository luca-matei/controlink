import socket
import logging

from controlink.utils import get_primary_ip


class Client:
    def __init__(self, host, port=65432):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            logging.info(f"Connected to {self.host}:{self.port}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    logging.info("Connection closed by server.")
                    break
                logging.info(f"Mouse position: {data.decode('utf-8')}")


def main():
    server_ip = get_primary_ip()
    client = Client(server_ip)
    try:
        client.run()
    except KeyboardInterrupt:
        logging.info("Exiting client.")


if __name__ == "__main__":
    main()
