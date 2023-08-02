import zmq
import inspect
from PyQt5 import QtCore

from qapp.plug import PlugApp

from .viewer import LuraView
from .modes import Normal, Command, Visual
from .utils import LuraDisplay, LuraBuffer

class Lura(PlugApp):

    actionRegistered=QtCore.pyqtSignal()

    def __init__(self): 

        super().__init__(
            respond_port=True,
            initiate_stack=True
            )

    def getActions(self):

        data={}
        for plug, actions in self.manager.actions.items():
            name=None
            plug_data=[]
            for d, a in actions.items():
                if hasattr(plug, 'name'):
                    name=plug.name
                else:
                    name=plug.__class__.__name__
                plug_data+=['_'.join(d)]

            if name: data[name]=plug_data

        return data

    def handle(self, request):

        response=super().handle(request)

        action=request.get('action', None)
        part=request.get('part', None)

        c1=response.get('status', 'nok')!='ok'

        if c1 or part:

            if part:
                obj=self
                parts=part.split('.')
                for p in parts: 
                    obj=getattr(obj, p, None)
                    print(p, obj)
                    if not obj: break
                func=getattr(obj, action, None)
                print('here', obj, func)
            else:
                func=self.manager.all_actions.get(action, None)
            
            if func:

                result=None
                prmts=inspect.signature(func).parameters

                if len(prmts)==0:
                    if action=='quit' and self.respond_port:
                        msg={'status':'ok', 'info':'quitting'}
                        self.socket.send_json(msg)
                        func()
                    else:
                        result=func()
                elif 'request' in prmts:
                    result=func(request)
                else:
                    fp={}
                    for p in prmts:
                        if p in request: fp[p]=request[p] 
                    result=func(**fp)
                response['status']='ok'
                response['result']=result
        return response

    def setConnection(self): 

        super().setConnection(zmq.REP)

    def setParser(self):

        super().setParser()

        self.parser.add_argument(
                'file', nargs='?', default=None, type=str)
        self.parser.add_argument(
                '-p', '--page', default=0, type=int)
        self.parser.add_argument(
                '-x', '--xaxis', default=0., type=float)
        self.parser.add_argument(
                '-y', '--yaxis', default=0., type=float)

    def setStack(self): super().setStack(LuraDisplay, LuraView)

    def setManager(self): super().setManager(buffer=LuraBuffer)

    def loadModes(self): 

        for m in [Normal, Command, Visual]: 
            self.modes.addMode(m(self))
        self.modes.setMode('normal')

    def parse(self):

        args, unkw = super().parse()

        if args.file:
            self.main.open(filePath=args.file)

        if args.page:
            view=self.main.display.currentView()
            if view: 
                view.goto(args.page, args.xaxis, args.yaxis)

def run():

    app=Lura()
    app.run()
