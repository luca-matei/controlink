import socket
import logging

from controlink.utils import get_primary_ip
from controlink.config import settings


class Client:
    def __init__(self):
        self.server_host = settings.client.server_host
        self.server_port = settings.client.server_port

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.server_host, self.server_port))
                logging.info(f"Connected to {self.server_host}:{self.server_port}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        logging.info("Connection closed by server.")
                        break
                    logging.info(f"Mouse position: {data.decode('utf-8')}")

        except ConnectionRefusedError:
            logging.error(
                f"Connection refused by {self.server_host}:{self.server_port}"
            )


def main():
    client = Client()
    try:
        client.run()
    except KeyboardInterrupt:
        logging.info("Exiting client.")


if __name__ == "__main__":
    main()
