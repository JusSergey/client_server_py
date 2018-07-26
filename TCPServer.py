import socket
import threading
from time import sleep


class TCPServer:
    def __init__(self):
        self.clients = []
        self.sock = socket.socket()
        pass

    def create_connection(self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address, int(port))
        self.sock.bind(server_address)
        return self.sock

    def wait_connection(self, clients=1):
        self.sock.listen(clients)
        client_sock, _ingnore = self.sock.accept()

    def non_block(self):
        self.sock.setbloking(0)

    def receive(self):
        while