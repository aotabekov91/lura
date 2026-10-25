import zmq

from PyQt6 import QtCore

class Broadcast(QtCore.QObject):

    broadcastReceived=QtCore.pyqtSignal(object)

    def __init__(self, brdcst_addr):
        super().__init__()
        self.activated=False
        self.setBroadcast(brdcst_addr)

    def setBroadcast(self, brdcst_addr):
        self.m_socket=zmq.Context().socket(zmq.SUB)
        self.m_socket.connect(brdcst_addr)
        self.m_socket.subscribe('')

    def startListen(self):
        self.activated=True
        while self.activated:
            data=self.m_socket.recv_json()
            self.broadcastReceived.emit(data)

    def finishListen(self):
        self.activated=False
