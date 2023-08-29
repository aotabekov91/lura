import inspect
from PyQt5 import QtCore

from plug.qt import PlugApp

from .view import View
from .utils import Display, Buffer

class Lura(PlugApp):

    actionRegistered=QtCore.pyqtSignal()

    def __init__(self, **kwargs): 

        super().__init__(
            respond_port=True,
            initiate_stack=True,
            **kwargs
            )

    def getActions(self):

        data={}
        for plug, actions in self.manager.actions.items():
            plug_data=[]
            if hasattr(plug, 'name'):
                name=plug.name
            else:
                name=plug.__class__.__name__
            for d, a in actions.items():
                plug_data+=['_'.join(d)]
            data[name]=plug_data

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

    def registerByUmay(self, path=None, kind=None):
        super().registerByUmay(path, kind='REQ')

    def setConnection(self): 
        super().setConnection(kind='REP')

    def setParser(self):

        super().setParser()

        self.parser.add_argument(
                'file',
                nargs='?',
                default=None,
                type=str)
        self.parser.add_argument(
                '-p',
                '--page',
                default=0,
                type=int)
        self.parser.add_argument(
                '-x',
                '--xaxis',
                default=0.,
                type=float)
        self.parser.add_argument(
                '-y', 
                '--yaxis', 
                default=0., 
                type=float)

    def setup(self): 

        super().setup()

        self.setParser()
        self.buffer=Buffer(self)
        self.setPlugman()
        self.setGUI(
            display_class=Display, 
            view_class=View)
        self.plugman.load()

    def parse(self):

        args, unkw = super().parse()

        if args.file:
            self.window.main.open(
                    filePath=args.file)

        view=self.window.main.display.currentView()

        if args.page and view:

            view.goto(
                    args.page, 
                    args.xaxis, 
                    args.yaxis)

def run():

    app=Lura()
    app.run()
