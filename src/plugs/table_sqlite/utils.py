import zmq

from PyQt6 import QtCore

from zmq_server import BroadcastServer

def ping(ip_addr):
    return BroadcastServer.query(
            ip_addr, {'action': 'pong'})

class Shell(QtCore.QObject):

    tableChanged=QtCore.pyqtSignal(object)

    def __init__(self, agent, name, database, fields):
        super().__init__()
        self.m_fields=[]
        self.m_agent=agent
        self.m_idx=id(self)
        self.setFields(fields)
        self.setName(database, name)

    def setName(self, database, name):
        database=database or name
        self.m_name=f'{database}_{name}'

    def setFields(self, fields):
        for field in fields:
            values=field.split(' ')
            if values:
                self.m_fields+=[values[0]]

    def name(self):
        return self.m_name

    def index(self):
        return self.m_idx

    def filterData(self, action, args, kwargs):
        if action in ['updateRow', 'writeRow']:
            filter_data={}
            data=kwargs.get('data', None)
            if data:
                for key, value in data.items():
                    if key in self.m_fields:
                        filter_data[key]=value
            kwargs['data']=filter_data

    def activate(
            self, 
            *args, 
            action=None,
            **kwargs,
            ):
        self.filterData(action, args, kwargs)
        result=self.m_agent.activate(
                *args, 
                **kwargs,
                action=action,
                connector_id=self.m_name, 
                connector_idx=self.m_idx)
        return result

class Broadcast(QtCore.QObject):

    broadcastReceived=QtCore.pyqtSignal(object)

    def __init__(self, ip):
        super().__init__()
        self.activated=False
        self.setBroadcast(ip)

    def setBroadcast(self, ip):
        self.m_socket=zmq.Context().socket(zmq.SUB)
        self.m_socket.connect(ip)
        self.m_socket.subscribe('')

    def startListen(self):
        self.activated=True
        while self.activated:
            data=self.m_socket.recv_json()
            self.broadcastReceived.emit(data)
