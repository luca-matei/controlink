from pynput import mouse
from controlink.utils import get_monitors


class Client:
    def __init__(self):
        self.monitors = get_monitors()

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
            print('Left margin')
        elif x == monitor.x + monitor.width - 1:
            print('Right margin')
        elif y == monitor.y:
            print('Top margin')
        elif y == monitor.y + monitor.height - 1:
            print('Bottom margin')

    def on_move(self, x, y):
        self.detect_margin(x, y)


def main():
    client = Client()

    with mouse.Listener(
            on_move=client.on_move) as listener:
        listener.join()


if __name__ == '__main__':
    main()
