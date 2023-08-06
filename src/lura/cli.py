import json

from plug import Plug

class LuraCLI(Plug):

    def __init__(self):

        super(LuraCLI, self).__init__(listen_port=False)

    def setParser(self):

        super().setParser()

        self.parser.add_argument('command')
        self.parser.add_argument('-p', '--part')

    def setConnection(self): 

        self.socket = self.getConnection(kind='REQ')
        self.socket.connect(f'tcp://localhost:{self.port}')

    def modeAction(self, mode, action, request={}):

        request['part']=mode
        request['action']=action

        self.socket.send_json(request)
        response=self.socket.recv_json()
        json_object = json.dumps(response, indent = 4) 
        print(json_object)

    def run(self):

        args, unkw = self.parser.parse_known_args()

        request={}
        for i in range(0, len(unkw), 2):
            request[unkw[i][2:]]=unkw[i+1]
        if args.command:
            self.modeAction(args.part, args.command, request)

def run():

   app=LuraCLI()
   app.run()
