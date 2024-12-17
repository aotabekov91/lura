import sys

from zmq_server import BroadcastServer

from table import Table

class Handler:

    def __init__(self):
        self.m_tables={}

    def act(
            self, 
            connector_id, 
            connector_idx, 
            *args, 
            **kwargs
            ):
        table=self.m_tables.get(connector_id)
        reply={
              'result': [], 
              'status': 'ok', 
              'connector_id': connector_id,
              'connector_idx': connector_idx,
              }
        if table:
            reply['result']=table.activate(*args, **kwargs)
        return reply 

    def createTable(
            self, 
            connector_id, 
            connector_idx, 
            *args, 
            **kwargs
            ):
        table=self.m_tables.get(connector_id, None)
        if not table:
            table=Table(*args, **kwargs)
            self.m_tables[connector_id]=table
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

    def __call__(self, request={}):
        args=request.get('args', [])
        kwargs=request.get('kwargs', {})
        action=request.get('action', None)
        connector_id=request.get(
                'connector_id', None)
        connector_idx=request.get(
                'connector_idx', None)
        if action=='create':
            return self.createTable(
                    connector_id, 
                    connector_idx,
                    *args, 
                    **kwargs
                    )
        else:
            return self.act(
                    connector_id, 
                    connector_idx,
                    *args, 
                    **kwargs,
                    action=action,
                    )

def create(ip_addr):
    server=BroadcastServer(handler=Handler(), sip_addr=ip_addr)
    server.run()

if __name__=='__main__':
    ip_addr=sys.argv[1]
    create(ip_addr)
