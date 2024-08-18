from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ZMQListener(QObject):

    request = pyqtSignal(dict)

    def __init__(self, parent):

        super(ZMQListener, self).__init__()
        self.parent = parent

    def loop(self):

        while self.parent.running:
            request = self.parent.socket.recv_json()
            self.request.emit(request)
