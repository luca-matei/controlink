import socket
import orjson

from loguru import logger
from pynput.mouse import Controller

from controlink.config import settings
from controlink.host import Host


class Client(Host):
    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.server_host = settings.client.server_host
        self.server_port = settings.client.server_port
        self.registered_commands = [
            "move_cursor",
            "delta_move_cursor",
        ]
        self.mouse = Controller()

    def move_cursor(self, x: int, y: int):
        """
        Move cursor using pynput
        """
        logger.info(f"Moving cursor to {x}, {y}")
        self.mouse.position = (x, y)

        if self.detect_margin(x, y) == "left":
            print("LEFT")
            self.send_message({
                "cmd": "gain_control",
                "args": {}
            })

    def delta_move_cursor(self, dx: int, dy: int):
        x, y = self.mouse.position
        x += dx
        y += dy
        self.move_cursor(x, y)

    def send_message(self, message: dict):
        self.client_socket.sendall(orjson.dumps(message))

    def process_message(self, data):
        message = orjson.loads(data)
        command = message.get("cmd")
        args = message.get("args")

        if command in self.registered_commands:
            getattr(self, command)(**args)

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client_socket:
                self.client_socket.connect((self.server_host, self.server_port))
                logger.info(f"Connected to {self.server_host}:{self.server_port}")

                while True:
                    data = self.client_socket.recv(1024)
                    if not data:
                        logger.info("Connection closed by server.")
                        break

                    try:
                        self.process_message(data)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")

        except ConnectionRefusedError:
            logger.error(f"Connection refused by {self.server_host}:{self.server_port}")


def main():
    client = Client()
    try:
        client.run()
    except KeyboardInterrupt:
        logger.info("Exiting client.")


if __name__ == "__main__":
    main()
