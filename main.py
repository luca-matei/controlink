import sys
from controlink import server, client


def main():
    if '--server' in sys.argv:
        server.main()
    elif '--client' in sys.argv:
        client.main()
    else:
        print('Usage:')
        print('pipenv run python3 main.py --server')
        print('pipenv run python3 main.py --client')


if __name__ == '__main__':
    main()
