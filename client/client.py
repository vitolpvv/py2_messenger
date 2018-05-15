import socket
import sys


class Client:

    def __init__(self, address, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))

    def close(self):
        self._socket.close()


if __name__ == '__main__':

    _DEFAULT_ADDRESS = 'localhost'
    _DEFAULT_PORT = 7777
    _IN_PARAM_ADDRESS_INDEX = 1
    _IN_PARAM_PORT_INDEX = 2

    addr = None
    p = None
    client = None

    try:
        addr = sys.argv[_IN_PARAM_ADDRESS_INDEX]
    except (ValueError, IndexError):
        addr = _DEFAULT_ADDRESS

    try:
        p = int(sys.argv[_IN_PARAM_PORT_INDEX])
    except (ValueError, IndexError):
        p = _DEFAULT_PORT

    try:
        client = Client(addr, p)
        print('Клиент подключен:', (addr, p))
    except ConnectionRefusedError as e:
        print('Ошибка подключения:', e.strerror)

    if client:
        try:
            client.close()
        except Exception as e:
            print('Ошибка взаимодействия:', e.args)
