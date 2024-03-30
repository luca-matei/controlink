from controlink.utils import get_monitors


class Host:
    def __init__(self):
        self.monitors = get_monitors()

    def get_current_monitor(self, x, y):
        for monitor in self.monitors:
            if (
                monitor.x <= x <= monitor.x + monitor.width
                and monitor.y <= y <= monitor.y + monitor.height
            ):
                return monitor

    def detect_margin(self, x, y):
        """
        Detect if the cursor is at the edge of the screen
        """
        monitor = self.get_current_monitor(x, y)
        if x == monitor.x:
            return "left"
        elif x == monitor.x + monitor.width - 1:
            return "right"
        elif y == monitor.y:
            return "top"
        elif y == monitor.y + monitor.height - 1:
            return "bottom"
        return None
