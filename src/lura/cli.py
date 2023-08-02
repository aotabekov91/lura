import zmq

from plug import Plug

class LuraCLI(Plug):

    def __init__(self):

        super(LuraCLI, self).__init__(listen_port=False)

    def setParser(self):

        super().setParser()

        self.parser.add_argument('command')
        self.parser.add_argument('-m', '--mode')

    def setConnection(self): 

        self.socket = zmq.Context().socket(zmq.PUSH)
        self.socket.connect(f'tcp://localhost:{self.port}')

    def modeAction(self, mode, action, request={}):

        request['mode']=mode
        request['action']=action
        self.socket.send_json(request)

    def run(self):

        args, unkw = self.parser.parse_known_args()

        request={}
        for i in range(0, len(unkw), 2):
            request[unkw[i][2:]]=unkw[i+1]
        if args.command:
            self.modeAction(args.mode, args.command, request)

def run():

   app=LuraCLI()
   app.run()
