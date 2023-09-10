import inspect

from plug.qt import PlugApp

from .view import View
from .utils import Display, Buffer

class Lura(PlugApp):

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

    def setup(self): 

        super().setup()
        self.buffer=Buffer(self)
        self.setGUI(
                display_class=Display, 
                view_class=View)

    def initialize(self):

        super().initialize()
        self.parser=self.plugman.plugs.get(
                'Parser', None)

    def parse(self):

        if self.parser:
            args, unkw = self.parser.parse()
            view=self.window.main.display.currentView()
            if args.file:
                self.window.main.open(
                        filePath=args.file)
            if args.page and view:
                view.goto(args.page, 
                          args.xaxis, 
                          args.yaxis)

    def run(self):

        self.parse()
        super().run()

def run():

    app=Lura()
    app.run()
