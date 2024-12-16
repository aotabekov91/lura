class ZMQServer:

    def __init__(
            self,
            handler=None,
            sip_addr=None,
            bip_addr=None,
            **kwargs,
            ):
        self.m_running=False
        self.m_kwargs=kwargs
        self.m_handler=handler
        self.m_sip_addr=sip_addr
        self.m_bip_addr=bip_addr
        self.setup()

    def setup(self):
        self.setConnection()

    def serverIP(self):
        return self.m_sip_addr

    def broadcastIP(self):
        return self.m_bip_addr

    def setConnection(self):
        # todo: only accept localhost or local network (not whole internet)
        self.m_sip_sock = zmq.Context().socket(zmq.REP)
        if self.m_sip_addr:
            self.m_sip_socket.bind(f'tcp://*:{self.m_sip_addr}')
        self.m_bip_sock = zmq.Context().socket(zmq.BROADCAST) # todo
        if self.m_bip_addr:
            self.m_bip_sock.bind(f'tcp://*:{self.m_sip_addr}')
        else:
            addr=self.m_bip_sock.bind_to_random_port(f'tcp://*')
            self.m_bip_addr=addr

    def pong(self):
        return {'status': 'ok'}

    @classmethod
    def ping(cls, ip_addr):
        # todo: poller while some n seconds and afterwards assume server is not 
        # running
        socket=zmq.Context().socket(zmq.REQ)
        socket.connect(ip_addr)
        socket.send_json({'action':'pong'})
        return socket.recv_json()
        
    def broadcast(self, data):
        self.m_bip_sock.send_json(data)

    def handler(self):
        return self.m_handler

    def setHandler(self, handler):
        self.m_handler=handler

    def handle(self, request):
        action=request.get('action', None)
        if action=='pong':
            return self.pong()
        elif self.m_handler:
            return self.m_handler(request)
        return {'status': 'nok', 'info': 'not understood'}

    def stop(self):
        self.m_running=False

    def run(self):
        self.m_running=True
        while self.m_running:
            request=self.m_sip_sock.recv_json()
            reply=self.handle(request)
            self.m_sip_sock.send_json(reply)
