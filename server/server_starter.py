import sys
import time
import select
import logging
import log_config
from server import Server
sys.path.append('..')
import jim.protocol as protocol
from log.log_deco import Log


@Log(logging.getLogger('server'))
def _validation(server, clients, new_clients, valid_clients):
    for client in clients:
        try:
            msg = server.read(client)
            msg = server.parse(msg)

            if msg.get(protocol.Message.KEY_ACTION) == protocol.Message.ACTION_PRESENCE:
                print('Клиент прошел валидацию и подключен к общему чату:', client.getpeername())
                valid_clients.append(client)
                server.send_response(client, protocol.Code.C_200)
            else:
                print('Ошибка валидации клинта. Клиент отключен:', client.getpeername())
                client.close()

            new_clients.pop(client)
        except:
            print('Ошибка валидации клинта. Клиент отключен:', client.getpeername())
            new_clients.pop(client)
            client.close()


def _read_requests(server, clients, valid_clients):
    messages = []
    for client in clients:
        try:
            msg = server.read(client)
            msg = server.parse(msg)
            print('Получено сообщение от', client.getpeername(), ':', msg)

            if msg.get(protocol.Message.KEY_ACTION) == protocol.Message.ACTION_QUIT:
                server.send_response(client, protocol.Code.C_200)
                raise Exception

            if msg.get(protocol.Message.KEY_ACTION) == protocol.Message.ACTION_MSG:
                server.send_response(client, protocol.Code.C_200)
                messages.append(msg)
        except:
            print('Клиент отключен:', client.getpeername())
            valid_clients.pop(valid_clients.index(client))
            client.close()

    return messages


def _send_messages(server, clients, messages, valid_clients):
    for message in messages:
        for client in clients:
            try:
                server.send(client, protocol.Converter.to_bytes(message))
            except:
                valid_clients.pop(valid_clients.index(client))
                client.close()


if __name__ == '__main__':

    _DEFAULT_ADDRESS = ''
    _DEFAULT_PORT = 7777
    _IN_PARAM_ADDR = '-a'
    _IN_PARAM_PORT = '-p'
    _ACCEPT_TIMEOUT = 0.2
    _VALIDATION_TIMEOUT = 5

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
        server = Server(addr, p, 100, 0.2)
        print('Сервер запущен:', server.get_name())
    except OSError as e:
        print('Ошибка запуска:', e.strerror)

    new_clients = {}

    valid_clients = []

    messages_to_send = []

    if server:
        print('Сервер ожидает подключения...')
        try:
            while True:
                try:
                    client_socket, client_address = server.accept()
                except OSError:
                    pass
                else:
                    print('Подключен новый клиент:', client_address)
                    new_clients[client_socket] = time.time()
                finally:
                    current_time = time.time()
                    for client, conn_time in new_clients.copy().items():
                        if current_time - conn_time > _VALIDATION_TIMEOUT:
                            print('Вышло время вылидации клиента. Клиент отключен:', client.getpeername())
                            new_clients.pop(client)
                            client.close()

                    try:
                        writers, _, _ = select.select(new_clients.keys(), [], [])
                    except OSError as e:
                        pass
                    else:
                        _validation(server, writers, new_clients, valid_clients)

                    try:
                        writers, readers, _ = select.select(valid_clients, valid_clients, [])
                    except OSError as e:
                        pass
                    else:
                        messages = _read_requests(server, writers, valid_clients)
                        _send_messages(server, readers, messages, valid_clients)
        finally:
            server.close()
