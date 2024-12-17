import os
import sys
import subprocess

from plug import Plug
from zmq_server import BroadcastServer

from .table import Table
from .utils import Shell, ping

class SQLiteTable(Plug):

    server_addr='tcp://localhost:19999'

    def setup(self):
        super().setup()
        self.setServer()

    def setServer(self):
        self.m_server=BroadcastServer
        pong=ping(self.server_addr)
        if not pong:
            server_script=os.path.join(
                    self.path, 'server.py')
            cmd=[sys.executable, server_script, self.server_addr]
            subprocess.Popen(cmd)

    def createTable(self, *args, **kwargs):
        if self.m_server:
            fields=kwargs.get(
                    'fields', [])
            table_name=kwargs.get(
                    'table_name', None)
            database_name=kwargs.get(
                    'database_name', None)
            database_name=None,
            connector=Shell(
                    agent=self,
                    fields=fields,
                    name=table_name,
                    database=database_name)
            connector_id=connector.name()
            connector_idx=connector.index()
            self.createQuery(
                    *args, 
                    **kwargs, 
                    connector_id=connector_id,
                    connector_idx=connector_idx,
                    )
            return connector
        else:
            return Table(*args, **kwargs)

    def createQuery(
            self, 
            *args, 
            connector_id=None,
            connector_idx=None,
            **kwargs,
            ):
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
