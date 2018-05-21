import socket
import sys
import jim.protocol as protocol


class Server:

    def __init__(self, address, port, count=5):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((address, port))
        self._socket.listen(count)

    def get_name(self):
        return self._socket.getsockname()

    def accept(self):
        return self._socket.accept()

    @staticmethod
    def send(client, message):
        client.send(message)

    def send_response(self, client, code, text=None):
        self.send(client, protocol.Message.response(code, text))

    @staticmethod
    def read(client):
        return client.recv(protocol.Message.get_max_length())

    @staticmethod
    def parse(message):
        return protocol.Message.parse(message)

    def close(self):
        self._socket.close()


if __name__ == '__main__':

    _DEFAULT_ADDRESS = ''
    _DEFAULT_PORT = 7777
    _IN_PARAM_ADDR = '-a'
    _IN_PARAM_PORT = '-p'

    addr = None
    p = None
    server = None

    try:
        addr = sys.argv[sys.argv.index(_IN_PARAM_ADDR) + 1]
    except (ValueError, IndexError):
        addr = _DEFAULT_ADDRESS

    try:
        p = int(sys.argv[sys.argv.index(_IN_PARAM_PORT) + 1])
    except (ValueError, IndexError):
        p = _DEFAULT_PORT

    try:
        server = Server(addr, p)
        print('Сервер запущен:', server.get_name())
    except OSError as e:
        print('Ошибка запуска:', e.strerror)

    if server:
        try:
            while True:
                print('Сервер ожидает подключения...')
                client_socket, client_address = server.accept()
                print('Подключен клиент: {}'.format(client_address))

                msg = server.read(client_socket)
                msg = server.parse(msg)
                print('Получено от {}: {}'.format(client_address, msg))
                
                if msg.get(protocol.Message.KEY_ACTION) == protocol.Message.ACTION_PRESENCE:
                    server.send_response(client_socket, protocol.Code.C_200)

                client_socket.close()
        finally:
            server.close()
