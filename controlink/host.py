import socket
from pynput import mouse
from controlink.utils import get_monitors


class Host:
    def __init__(self):
        self.monitors = get_monitors()
        self.server = None
        self.client = None

    def start(self):
        self.start_socket_server()
        self.track_input()

    def start_socket_server(self):
        """
        Start a socket server.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 65432))
        self.server.listen()

        self.client, address = self.server.accept()

    def track_input(self):
        """
        Track mouse input.
        """
        with mouse.Listener(
                on_move=self.on_move) as listener:
            listener.join()

    def send_message(self, message):
        """
        Send a message to the client.
        """
        self.client.sendall(message.encode('utf-8'))

    def get_current_monitor(self, x, y):
        """
        Returns the monitor where the pointer is located.
        """
        for monitor in self.monitors:
            if monitor.x <= x <= monitor.x + monitor.width and monitor.y <= y <= monitor.y + monitor.height:
                return monitor

    def detect_margin(self, x, y):
        """
        Detects if the pointer is at the margin of the screen.
        """
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


def main():
    host = Host()
    host.start()
