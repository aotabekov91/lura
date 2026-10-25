import zmq

from PyQt6 import QtCore

class Shell(QtCore.QObject):

    tableChanged=QtCore.pyqtSignal(object)

    def __init__(self, agent, name, database, fields, server_addr):
        super().__init__()
        self.m_fields=[]
        self.m_agent=agent
        self.setIndex(id(self))
        self.server_addr=server_addr
        self.setFields(fields)
        self.setName(database, name)

    @classmethod
    def query(cls, ip_addr, query):
        socket=zmq.Context().socket(zmq.REQ)
        socket.connect(ip_addr)
        socket.send_json(query)
        poller=zmq.Poller()
        poller.register(socket, flags=zmq.POLLIN)
        if poller.poll(timeout=1000):
            replay=socket.recv_json()
        else:
            socket.setsockopt(zmq.LINGER, 1)
            replay={}
        poller.unregister(socket)
        return replay

    @classmethod
    def ping(cls, ip_addr):
        return cls.query(ip_addr, {'action': 'pong'})

    def setIndex(self, idx):
        self.m_idx=idx

    def setName(self, database, name):
        database=database or name
        self.m_name=f'{database}_{name}'

    def setFields(self, fields):
        for field in fields:
            values=field.split(' ')
            if values:
                self.m_fields+=[values[0]]

    def index(self):
        return self.m_idx

    def name(self):
        return self.m_name

    def fields(self):
        return self.m_fields

    def filterData(self, action, args, kwargs):
        if action in ['updateRow', 'writeRow']:
            filter_data={}
            data=kwargs.get('data', None)
            if data:
                for key, value in data.items():
                    if key in self.m_fields:
                        filter_data[key]=value
            kwargs['data']=filter_data

    def createQuery(self, *args, **kwargs):
        connector_id=self.m_name
        connector_idx=self.m_idx
        request={
                'args': args, 
                'kwargs': kwargs,
                'action':'create', 
                'connector_id': self.m_name,
                'connector_idx': self.m_idx,
                }
        return self.query(self.server_addr, request)

    def activate(self, *args, action=None, **kwargs):
        self.filterData(action, args, kwargs)
        if action:
            request={
                    'args': args, 
                    'kwargs': kwargs,
                    'action': action,
                    'connector_id': self.m_name,
                    'connector_idx': self.m_idx,
                    }
            reply=self.query(self.server_addr, request)
            return reply.get('result', None)
