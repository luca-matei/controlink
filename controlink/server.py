import socket
import time
import orjson
import threading
from loguru import logger
from pynput.mouse import Listener, Controller

from controlink.host import Host
from controlink.utils import get_primary_ip


class Server(Host):
    def __init__(self, host=None, port=65432):
        super().__init__()
        self.host = host or get_primary_ip()
        self.port = port
        self.clients = {}  # Dictionary to manage multiple connections
        self.has_control = True
        self.margin_map = {"left": None, "right": None, "top": None, "bottom": None}
        self.listener = Listener(on_move=self.on_move)
        self.registered_commands = [
            "gain_control",
        ]
        self.center_x = self.monitors[0].width // 2
        self.center_y = self.monitors[0].height // 2
        self.control_client = None
        self.mouse = Controller()

    def track_input(self):
        self.listener.start()

    def check_margin(self, x, y):
        client_conn = None

        margin = self.detect_margin(x, y)
        if margin:
            client_conn = self.margin_map.get(margin)

        if client_conn:
            self.send_message(
                client_conn,
                {
                    "cmd": "move_cursor",
                    "args": {
                        "x": 10,
                        "y": 10,
                    },
                },
            )
            self.control_client = client_conn
            self.has_control = False
            logger.info("Lost control.")

    def gain_control(self):
        logger.info("Gained control.")
        self.has_control = True

    def move_cursor_to_center(self):
        self.mouse.position = (self.center_x, self.center_y)

    def on_move(self, x, y):
        if self.has_control:
            self.check_margin(x, y)
        else:
            dx = x - self.center_x
            dy = y - self.center_y

            direction = {"dx": 0, "dy": 0}
            if dx != 0:
                direction["dx"] = int(dx / abs(dx))  # 1 for right, -1 for left
            if dy != 0:
                direction["dy"] = int(dy / abs(dy))  # 1 for down, -1 for up

            # Send the direction message if there was any movement
            if dx != 0 or dy != 0:
                self.send_message(
                    self.control_client, {"cmd": "delta_move_cursor", "args": direction}
                )

            self.move_cursor_to_center()

    def send_message(self, conn, message: dict):
        if conn in self.clients:
            try:
                conn.sendall(orjson.dumps(message))
            except BrokenPipeError:
                logger.error("Connection closed by client.")
                self.clients.pop(conn, None)

    def process_messages(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break  # Connection closed by client
                message = orjson.loads(data)

                command = message.get("cmd")
                args = message.get("args")

                if command in self.registered_commands:
                    getattr(self, command)(**args)

            except ConnectionResetError:
                break  # Connection reset by client
        conn.close()
        self.clients.pop(conn, None)
        logger.info("Client disconnected.")

    def handle_client(self, conn, addr):
        self.clients[conn] = addr
        logger.info(f"Connected by {addr}")
        self.margin_map["right"] = conn
        # Start a new thread to process messages from this client
        thread = threading.Thread(target=self.process_messages, args=(conn,))
        thread.daemon = True
        thread.start()

    def run(self):
        self.track_input()
        logger.info("Started tracking input.")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logger.info(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()


def main():
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server shutting down.")
        server.listener.stop()


if __name__ == "__main__":
    main()
