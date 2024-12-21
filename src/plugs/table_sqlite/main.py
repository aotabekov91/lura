import os
import sys
import subprocess

from PyQt6 import QtCore

from plug import Plug
from zmq_server import BroadcastServer

from .table import Table
from .utils import Shell, Broadcast, ping

class SQLiteTable(Plug, QtCore.QObject):

    server_addr='tcp://localhost:19999'

    def setup(self):
        super().setup()
        self.setServer()
        self.m_connectors={}

    def setServer(self):
        self.m_server=BroadcastServer
        pong=ping(self.server_addr)
        if not pong:
            server_script=os.path.join(
                    self.path, 'server.py')
            cmd=[sys.executable, server_script, self.server_addr]
            subprocess.Popen(cmd)
        request={'action': 'info'}
        reply=self.m_server.query(self.server_addr, request)
        broadcast_ip=reply.get('broadcast_ip', None)
        self.setBroadcast(broadcast_ip)

    def createTable(self, *args, **kwargs):
        if self.m_server:
            fields=kwargs.get(
                    'fields', [])
            table_name=kwargs.get(
                    'table_name', None)
            database_name=kwargs.get(
                    'database_name', None)
            connector=Shell(
                    agent=self,
                    name=table_name,
                    database=database_name,
                    fields=fields,
                    )
            self.createQuery(
                    *args, 
                    **kwargs, 
                    connector=connector
                    )
            self.saveConnector(connector)
            return connector
        else:
            return Table(*args, **kwargs)

    def saveConnector(self, connector):
        name=connector.name()
        if not name in self.m_connectors:
            self.m_connectors[name]=[]
        self.m_connectors[name]+=[connector]

    def createQuery(
            self, 
            *args, 
            connector=None,
            **kwargs,
            ):
        if connector:
            connector_id=connector.name()
            connector_idx=connector.index()
            request={
                    'args': args, 
                    'kwargs': kwargs,
                    'action':'create', 
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    }
            self.m_server.query(self.server_addr, request)

    def activate(
            self, 
            *args, 
            action=None, 
            connector_id=None,
            connector_idx=None,
            **kwargs,
            ):
        if action:
            request={
                    'args': args, 
                    'kwargs': kwargs,
                    'action': action,
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    }
            reply=self.m_server.query(
                    self.server_addr, request)
            return reply.get('result', None)

    def handleBroadcast(self, data):
        connector_id=data.get('connector_id')
        connector_idx=data.get('connector_idx')
        connectors=self.m_connectors.get(connector_id, [])
        for connector in connectors:
            cid=connector.index()
            if cid!=connector_idx:
                connector.tableChanged.emit(data)

    def setBroadcast(self, ip):
        thread=QtCore.QThread()
        listener=Broadcast(ip)
        listener.broadcastReceived.connect(self.handleBroadcast)
        listener.moveToThread(thread)
        thread.started.connect(listener.startListen)
        self.m_listener=listener
        self.m_thread=thread
        thread.start()
