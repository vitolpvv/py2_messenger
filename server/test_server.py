import socket
import threading
import time
from server import Server


class TestServer:

    @staticmethod
    def run_fake_client():
        time.sleep(0.5)
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 7777))
        msg = fake_client.recv(1024)
        fake_client.send(msg)
        fake_client.close()

    def test_send_read(self):
        # запуск эхо-клиента в другом потоке
        client_thread = threading.Thread(target=self.run_fake_client)
        client_thread.start()

        send_msg = 'Hello, World!'

        messenger_server = Server('127.0.0.1', 7777)
        client, add = messenger_server.accept()
        client.send(send_msg.encode('utf-8'))
        recv_msg = client.recv(1024).decode('utf-8')

        assert send_msg == recv_msg

        client.close()
        messenger_server.close()

        client_thread.join()
