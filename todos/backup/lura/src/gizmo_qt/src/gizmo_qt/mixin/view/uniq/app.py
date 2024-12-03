import sys

from PyQt6 import QtNetwork


class UniqApp:
    canHide = True

    def setup(self):
        self.checkServer()
        super().setup()

    def checkServer(self):
        s = QtNetwork.QLocalSocket(self)
        s.errorOccurred.connect(self.prepareServer)
        s.connected.connect(self.requestServer)
        n = self.__class__.__name__
        s.connectToServer(n)

    def prepareServer(self, e):
        s = QtNetwork.QLocalSocket
        if e == s.ServerNotFoundError:
            s = QtNetwork.QLocalServer(self)
            s.newConnection.connect(self.respondServer)
            self.appIsLaunched.connect(self.runServer)
            self.appSoonQuits.connect(self.closeServer)
            self.m_server = s
        else:
            raise

    def closeServer(self):
        self.wait(1)
        self.m_server.close()
        self.wait(-1)

    def runServer(self):
        n = self.__class__.__name__
        self.m_server.listen(n)

    def respondServer(self):
        con = self.m_server.nextPendingConnection()
        con.disconnectFromServer()
        self.ui.activateWindow()
        self.ui.show()

    def requestServer(self):
        sys.exit()
