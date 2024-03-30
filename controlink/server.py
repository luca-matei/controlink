import socket
from pynput import mouse
from pynput.mouse import Listener
from controlink.utils import get_monitors


class Server:
    def __init__(self, host='0.0.0.0', port=65432):
        self.host = host
        self.port = port
        self.conn = None
        self.listener = Listener(on_move=self.on_move)
        self.monitors = get_monitors()

    def track_input(self):
        with mouse.Listener(on_move=self.on_move) as listener:
            listener.join()

    def get_current_monitor(self, x, y):
        for monitor in self.monitors:
            if monitor.x <= x <= monitor.x + monitor.width and monitor.y <= y <= monitor.y + monitor.height:
                return monitor

    def detect_margin(self, x, y):
        monitor = self.get_current_monitor(x, y)
        if x == monitor.x:
            self.send_message('Left margin')
        elif x == monitor.x + monitor.width - 1:
            self.send_message('Right margin')
        elif y == monitor.y:
            self.send_message('Top margin')
        elif y == monitor.y + monitor.height - 1:
            self.send_message('Bottom margin')

    def on_move(self, x, y):
        self.detect_margin(x, y)

    def send_message(self, message):
        if self.conn:
            self.conn.sendall(message.encode('utf-8'))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable SO_REUSEADDR
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")
            self.conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with self.conn:
                self.track_input()  # Changed to track_input to ensure correct listener usage


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
