import sys
from client import Client
sys.path.append('..')
import jim.protocol as protocol


def _read(client):
    while True:
        msg = client.read()
        msg = client.parse(msg)
        print('Получено сообщение от', msg.get(protocol.Message.KEY_MSG_FROM), ':', msg.get(protocol.Message.KEY_MSG_MESSAGE))


def _write(client):
    while True:
        msg = input('Введите сообщение:')
        if msg:
            client.send(protocol.Message.request_message(client.get_name(), '#All', msg))
            msg = client.parse(client.read())
            print('Получен ответ:', protocol.Code.get_description(msg.get(protocol.Message.KEY_RESPONSE)))


if __name__ == '__main__':
    _DEFAULT_ADDRESS = 'localhost'
    _DEFAULT_PORT = 7777
    _DEFAULT_NAME = 'Guest'
    _IN_PARAM_ADDRESS = '-a'
    _IN_PARAM_PORT = '-p'
    _IN_PARAM_WRITER = '-w'
    _IN_PARAM_READER = '-r'
    _IN_PARAM_NAME = '-n'

    addr = None
    p = None
    client = None
    writer = False
    reader = False
    name = None

    try:
        addr = sys.argv[sys.argv.index(_IN_PARAM_ADDRESS) + 1]
    except (ValueError, IndexError):
        addr = _DEFAULT_ADDRESS

    try:
        p = int(sys.argv[sys.argv.index(_IN_PARAM_PORT) + 1])
    except (ValueError, IndexError):
        p = _DEFAULT_PORT

    try:
        name = sys.argv[sys.argv.index(_IN_PARAM_NAME) + 1]
    except (ValueError, IndexError):
        name = _DEFAULT_NAME

    try:
        sys.argv.index(_IN_PARAM_READER)
        reader = True
    except ValueError:
        pass

    try:
        sys.argv.index(_IN_PARAM_WRITER)
        writer = True
    except ValueError:
        pass

    try:
        client = Client(addr, p, name)
        print('Клиент подключен:', (addr, p))
    except ConnectionRefusedError as e:
        print('Ошибка подключения:', e.strerror)

    if client:
        try:
            print('Отправка сообщения о присутствии')
            client.send(protocol.Message.request_presence(client.get_name()))

            msg = client.read()
            msg = client.parse(msg)
            print('Получен ответ:', protocol.Code.get_description(msg.get(protocol.Message.KEY_RESPONSE)))

            if reader:
                _read(client)
            elif writer:
                _write(client)
        except Exception as e:
            print('Ошибка взаимодействия:', e.args)
        finally:
            client.close()
