# -*- coding: utf-8 -*-

from socket import socket
from core.QtModules import pyqtSignal, pyqtSlot, QThread
from core import main as mn


class Socket(QThread):

    """Connection object."""

    receive = pyqtSignal(str)

    def __init__(self):
        super(Socket, self).__init__()
        self.socket = socket()
        self.address = "127.0.0.1"
        self.port = 5000

    def connect(self, address: str, port: int):
        self.address = address
        self.port = port

    def run(self):
        try:
            self.socket.connect((self.address, self.port))
        except ConnectionRefusedError:
            return

        while True:
            try:
                data = self.socket.recv(5000)
            except ConnectionAbortedError:
                return
            else:
                self.receive.emit(data.decode('utf-8'))

    def close(self):
        try:
            self.socket.close()
        except ConnectionRefusedError:
            pass
        else:
            # Recreate a new socket object.
            self.socket = socket()

    @pyqtSlot(str)
    def send(self, text: str):
        try:
            self.socket.send(text.encode('utf-8'))
        except (ConnectionRefusedError, OSError):
            return
