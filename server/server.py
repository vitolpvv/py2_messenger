import socket
import sys


class Server:

    def __init__(self, address, port, count=5):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((address, port))
        self._socket.listen(count)

    def accept(self):
        return self._socket.accept()

    def close(self):
        self._socket.close()


if __name__ == '__main__':

    _DEFAULT_ADDRESS = ''
    _DEFAULT_PORT = 7777
    _IN_PARAM_ADDR = '-a'
    _IN_PARAM_PORT = '-p'

    addr = None
    p = None

    try:
        addr = sys.argv[sys.argv.index(_IN_PARAM_ADDR) + 1]
    except (ValueError, IndexError):
        addr = _DEFAULT_ADDRESS

    try:
        p = int(sys.argv[sys.argv.index(_IN_PARAM_PORT) + 1])
    except (ValueError, IndexError):
        p = _DEFAULT_PORT

    s = Server(addr, p)
    print('Сервер запущен {}:{}'.format(addr, p))
    try:
        while True:
            print('Сервер ожидает подключения...')
            client_socket, client_address = s.accept()
            print('Подключен клиент: {}'.format(client_address))
            client_socket.close()
    except KeyboardInterrupt:
        s.close()
        print('Сервер остановлен')
