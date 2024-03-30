import screeninfo
import socket


def get_monitors():
    return screeninfo.get_monitors()


def get_primary_ip():
    """Get the primary IP address of the host."""
    try:
        # Create a dummy socket to a remote server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Google's public DNS server to find our IP address
            s.connect(("8.8.8.8", 80))
            # Get the socket's own address
            ip = s.getsockname()[0]
    except Exception as e:
        ip = "Error: Unable to get IP address - " + str(e)
    return ip
