import socket


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
    print('Скрипт запущен самостоятельно')
    s = Server('localhost', 8888)
    try:
        print('Сервер ожидает подключения...')
        while True:
            client_socket, address_address = s.accept()
    except KeyboardInterrupt:
        s.close()
