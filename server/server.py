import socket
import sys
sys.path.append('..')
import jim.protocol as protocol
from log.log_deco import Log
import logging
import log_config


class Server:

    def __init__(self, address, port, count=5, timeout=None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((address, port))
        self._socket.listen(count)
        if timeout:
            self._socket.settimeout(timeout)

    def get_name(self):
        return self._socket.getsockname()

    def accept(self):
        return self._socket.accept()

    @staticmethod
    @Log(logging.getLogger('server'))
    def send(client, message):
        client.send(message)

    @Log(logging.getLogger('server'))
    def send_response(self, client, code, text=None):
        self.send(client, protocol.Message.response(code, text))

    @staticmethod
    @Log(logging.getLogger('server'))
    def read(client):
        return client.recv(protocol.Message.get_max_length())

    @staticmethod
    @Log(logging.getLogger('server'))
    def parse(message):
        return protocol.Converter.from_bytes(message)

    @Log(logging.getLogger('server'))
    def close(self):
        self._socket.close()


if __name__ == '__main__':
    pass
