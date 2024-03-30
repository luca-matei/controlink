import sys
from controlink import host, client


def main():
    if '--host' in sys.argv:
        host.main()
    elif '--client' in sys.argv:
        client.main()
    else:
        print('Usage:')
        print('pipenv run python3 main.py --host')
        print('pipenv run python3 main.py --client')


if __name__ == '__main__':
    main()
