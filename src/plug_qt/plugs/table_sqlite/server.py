import sys

import zmq

from table import Table

class SQLiteServer:

    def __init__(self, sip_addr=None, bip_addr=None, **kwargs):
        self.m_running=False
        self.m_kwargs=kwargs
        self.m_sip_addr=sip_addr
        self.m_bip_addr=bip_addr
        self.setup()

    def setup(self):
        self.m_tables={}
        self.setConnection()

    def serverIP(self):
        return self.m_sip_addr

    def broadcastIP(self):
        return self.m_bip_addr

    def broadcast(self, request, result, args, kwargs, connector_id, connector_idx):
        action=request.get('action', None)
        if action in ['updateRow', 'writeRow', 'removeRow']:
            data={
                    'action': action,
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    'args': args,
                    'kwargs': kwargs,
                    'result': result,
                    'request': request,
                    }
            self.m_bip_sock.send_json(data)

    def setConnection(self):
        self.m_sip_sock = zmq.Context().socket(zmq.REP)
        if self.m_sip_addr:
            self.m_sip_sock.bind(f'{self.m_sip_addr}')
        self.m_bip_sock = zmq.Context().socket(zmq.PUB)
        if self.m_bip_addr:
            self.m_bip_sock.bind(f'{self.m_bip_addr}')
        else:
            addr=self.m_bip_sock.bind_to_random_port(f'tcp://*')
            self.m_bip_addr=f'tcp://localhost:{addr}'

    def createTable(self, connector_id, connector_idx, *args, **kwargs):
        table=self.m_tables.get(connector_id, None)
        if not table:
            self.m_tables[connector_id]=Table(*args, **kwargs)
            return {
                    'status':'ok', 
                    'info': 'created table',
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    }
        else:
            return {
                    'status':'ok', 
                    'info': 'table exists',
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    }

    def handle(self, request):
        action=request.get('action', None)
        if action in ['info', 'pong']:
            return {
                    'status': 'ok',
                    'server_ip': self.serverIP(),
                    'broadcast_ip': self.broadcastIP(),
                    }
        elif action=='stop':
            self.m_running=False
            return {'status': 'ok', 'info': 'stopping'}
        return self.handleQuery(request)

    def handleQuery(self, request={}):
        args=request.get('args', [])
        kwargs=request.get('kwargs', {})
        action=request.get('action', None)
        connector_id=request.get('connector_id', None)
        connector_idx=request.get('connector_idx', None)
        if action=='create':
            return self.createTable(connector_id, connector_idx, *args, **kwargs)
        else:
            table=self.m_tables.get(connector_id)
            reply={
                  'result': [], 
                  'status': 'ok', 
                  'connector_id': connector_id,
                  'connector_idx': connector_idx,
                  }
            if table:
                result=table.activate(*args, action=action, **kwargs)
                reply['result']=result
                self.broadcast(request, result, args, kwargs, connector_id, connector_idx)
            return reply 

    def run(self):
        self.m_running=True
        while self.m_running:
            request=self.m_sip_sock.recv_json()
            reply=self.handle(request)
            self.m_sip_sock.send_json(reply)

if __name__=='__main__':
    ip_addr=sys.argv[1]
    server=SQLiteServer(sip_addr=ip_addr)
    server.run()
