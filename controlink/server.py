import socket
import orjson

from loguru import logger
from pynput import mouse
from pynput.mouse import Listener
from controlink.utils import get_monitors, get_primary_ip


class Server:
    def __init__(self, host=None, port=65432):
        self.host = host or get_primary_ip()
        self.port = port
        self.conn = None
        self.listener = Listener(on_move=self.on_move)
        self.monitors = get_monitors()
        self.has_control = True

    def track_input(self):
        with mouse.Listener(on_move=self.on_move) as listener:
            listener.join()

    def get_current_monitor(self, x, y):
        for monitor in self.monitors:
            if (
                monitor.x <= x <= monitor.x + monitor.width
                and monitor.y <= y <= monitor.y + monitor.height
            ):
                return monitor

    def detect_margin(self, x, y):
        monitor = self.get_current_monitor(x, y)
        client_x = None
        client_y = None

        if x == monitor.x:
            # Cursor is at the left margin; move it to the right margin
            client_x = monitor.x + monitor.width - 2  # Position it just inside the right margin
            client_y = y
        elif x == monitor.x + monitor.width - 1:
            # Cursor is at the right margin; move it to the left margin
            client_x = monitor.x + 1  # Position it just inside the left margin
            client_y = y
        elif y == monitor.y:
            # Cursor is at the top margin; move it to the bottom margin
            client_x = x
            client_y = monitor.y + monitor.height - 2  # Position it just above the bottom margin
        elif y == monitor.y + monitor.height - 1:
            # Cursor is at the bottom margin; move it to the top margin
            client_x = x
            client_y = monitor.y + 1  # Position it just below the top margin

        if client_x is not None and client_y is not None:
            self.send_message({
                "cmd": "move_cursor",
                "args": {
                    "x": client_x,
                    "y": client_y,
                }
            })

            self.has_control = False

    def on_move(self, x, y):
        if self.has_control:
            self.detect_margin(x, y)
        else:
            logger.warning("Doesn't have control anymore.")

    def send_message(self, message: dict):
        if self.conn:
            try:
                self.conn.sendall(orjson.dumps(message))
            except BrokenPipeError:
                logger.error("Connection closed by client.")
                self.conn = None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )  # Enable SO_REUSEADDR
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logger.info(f"Server listening on {self.host}:{self.port}")
            self.conn, addr = server_socket.accept()
            logger.info(f"Connected by {addr}")
            with self.conn:
                self.track_input()


def main():
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server shutting down.")


if __name__ == "__main__":
    main()
