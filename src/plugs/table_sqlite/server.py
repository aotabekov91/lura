import sys

from zmq_server import BroadcastServer

from table import Table

class SQLiteServer(BroadcastServer):

    def setup(self):
        super().setup()
        self.m_tables={}
        self.setHandler(self)

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
            result=table.activate(*args, **kwargs)
            reply['result']=result
            self.checkBroadcast(result, args, kwargs, connector_id, connector_idx)
        return reply 

    def checkBroadcast(self, result, args, kwargs, connector_id, connector_idx):
        action=kwargs.get('action', None)
        if action in ['updateRow', 'writeRow', 'removeRow']:
            data={
                    'action': action,
                    'connector_id': connector_id,
                    'connector_idx': connector_idx,
                    'args': args,
                    'kwargs': kwargs,
                    'result': result,
                    }
            self.broadcast(data)

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
    server=SQLiteServer(sip_addr=ip_addr)
    server.run()

if __name__=='__main__':
    ip_addr=sys.argv[1]
    create(ip_addr)
