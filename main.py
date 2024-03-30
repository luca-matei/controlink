import sys
import logging

from controlink import server, client

logging.basicConfig(level=logging.INFO)


def main():
    if "--server" in sys.argv:
        server.main()
    elif "--client" in sys.argv:
        client.main()
    else:
        print("Usage:")
        print("pipenv run python3 main.py --server")
        print("pipenv run python3 main.py --client")


if __name__ == "__main__":
    main()
