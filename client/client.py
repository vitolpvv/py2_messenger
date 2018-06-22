import socket
import sys
sys.path.append('..')
import jim.protocol as protocol
from log.log_deco import Log
import logging
import log_config


class Client:

    def __init__(self, address, port, name='Guest', login=None, password=None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self._name = name
        self._login = login
        self._password = password

    @Log(logging.getLogger('client'))
    def send(self, message):
        self._socket.send(message)

    @Log(logging.getLogger('client'))
    def read(self):
        return self._socket.recv(protocol.Message.get_max_length())

    def get_name(self):
        return self._name

    @staticmethod
    @Log(logging.getLogger('client'))
    def parse(message):
        return protocol.Converter.from_bytes(message)

    @Log(logging.getLogger('client'))
    def close(self):
        self._socket.close()


if __name__ == '__main__':
    pass
