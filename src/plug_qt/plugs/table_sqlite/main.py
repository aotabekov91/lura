import os
import sys
import subprocess

from PyQt6 import QtCore

from plug import Plug

from .utils import Shell, Broadcast

class SQLiteTable(Plug, QtCore.QObject):

    server_addr='tcp://localhost:19999'

    def setup(self):
        super().setup()
        self.setServer()
        self.m_connectors={}

    def setServer(self):
        if not Shell.ping(self.server_addr):
            server_script=os.path.join(self.path, 'server.py')
            cmd=[sys.executable, server_script, self.server_addr]
            subprocess.Popen(cmd)
        request={'action': 'info'}
        reply=Shell.query(self.server_addr, request)
        broadcast_ip=reply.get('broadcast_ip', None)
        self.setBroadcast(broadcast_ip)

    def createTable(self, *args, **kwargs):
        fields=kwargs.get('fields', [])
        table_name=kwargs.get('table_name', None)
        database_name=kwargs.get('database_name', None)
        connector=Shell(
                agent=self,
                name=table_name,
                database=database_name,
                fields=fields,
                server_addr=self.server_addr)
        connector.createQuery(*args, **kwargs)
        self.saveConnector(connector)
        return connector

    def saveConnector(self, connector):
        name=connector.name()
        if not name in self.m_connectors:
            self.m_connectors[name]=[]
        self.m_connectors[name]+=[connector]

    def handleBroadcast(self, data):
        connector_id=data.get('connector_id')
        connector_idx=data.get('connector_idx')
        connectors=self.m_connectors.get(connector_id, [])
        for connector in connectors:
            cid=connector.index()
            if cid!=connector_idx:
                connector.tableChanged.emit(data)

    def setBroadcast(self, addrs):
        listener=Broadcast(addrs)
        listener.broadcastReceived.connect(self.handleBroadcast)
        thread=QtCore.QThread()
        listener.moveToThread(thread)
        thread.started.connect(listener.startListen)
        self.m_listener=listener
        self.m_thread=thread
        thread.start()
