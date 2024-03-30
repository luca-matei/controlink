import socket
import orjson

from loguru import logger
from pynput.mouse import Controller

from controlink.config import settings


class Client:
    def __init__(self):
        self.server_host = settings.client.server_host
        self.server_port = settings.client.server_port
        self.registered_commands = [
            "move_cursor",
        ]
        self.mouse = Controller()

    def move_cursor(self, x: int, y: int):
        """
        Move cursor using pynput
        """
        self.mouse.position = (x, y)

    def process_message(self, data):
        message = orjson.loads(data)
        command = message.get("cmd")
        args = message.get("args")

        if command in self.registered_commands:
            getattr(self, command)(**args)

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.server_host, self.server_port))
                logger.info(f"Connected to {self.server_host}:{self.server_port}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        logger.info("Connection closed by server.")
                        break

                    self.process_message(data)

        except ConnectionRefusedError:
            logger.error(
                f"Connection refused by {self.server_host}:{self.server_port}"
            )


def main():
    client = Client()
    try:
        client.run()
    except KeyboardInterrupt:
        logger.info("Exiting client.")


if __name__ == "__main__":
    main()
