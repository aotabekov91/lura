import zmq

class BroadcastServer:

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
        self.m_sip_sock = zmq.Context().socket(zmq.REP)
        if self.m_sip_addr:
            self.m_sip_sock.bind(f'{self.m_sip_addr}')
        self.m_bip_sock = zmq.Context().socket(zmq.PUB)
        if self.m_bip_addr:
            self.m_bip_sock.bind(f'{self.m_bip_addr}')
        else:
            addr=self.m_bip_sock.bind_to_random_port(f'tcp://*')
            self.m_bip_addr=f'tcp://localhost:{addr}'
            
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

    def pong(self):
        return {'status': 'ok'}

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
        elif action=='stop':
            return self.stop()
        elif self.m_handler:
            return self.m_handler(request)
        return {'status': 'nok', 'info': 'not understood'}

    def stop(self):
        self.m_running=False
        return {'status': 'ok', 'info': 'stopping'}

    def run(self):
        self.m_running=True
        while self.m_running:
            request=self.m_sip_sock.recv_json()
            reply=self.handle(request)
            self.m_sip_sock.send_json(reply)
