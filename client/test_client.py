import time
import socket
import threading
from client import Client


class TestClient:

    @staticmethod
    def run_echo_server():
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(('127.0.0.1', 7777))
        server_sock.listen()
        client_sock, addr = server_sock.accept()
        msg = client_sock.recv(1024)
        client_sock.send(msg)
        server_sock.close()

    def test_read_send(self):
        # запуск эхо-сервера в другом потоке
        server_thread = threading.Thread(target=self.run_echo_server)
        server_thread.start()

        time.sleep(0.5)

        msg_send = 'Hello, World'

        messenger_client = Client('127.0.0.1', 7777)
        messenger_client.send(msg_send.encode('utf-8'))
        msg_recv = messenger_client.read().decode('utf-8')

        assert msg_send == msg_recv

        server_thread.join()
