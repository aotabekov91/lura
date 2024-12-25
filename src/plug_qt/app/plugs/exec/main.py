import inspect
from collections import OrderedDict

from plug import Plug, tag

from .model import Model
from .view import ListView
from .overlay import OverlayView

class Exec(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        self.m_model=Model()
        if self.app.running:
            self.gatherCommands()
        else:
            self.app.appSoonStarts.connect(
                    self.gatherCommands)

    def setupView(self):
        self.m_overlay=OverlayView(
                app=self.app,
                view=self.app.view.main,
                identifier='O',
                objectName='ExecOverlay',
                )
        self.m_view=self.app.buffman.createView(
                ListView,
                app=self.app,
                name='ExecView',
                manager=self.m_overlay,
                parent=self.m_overlay,
                )
        self.m_view.setModel(self.m_model)
        self.m_model.rowsRemoved.connect(
                self.updateView)
        self.m_model.rowsInserted.connect(
                self.updateView)

    def updateView(self):
        self.m_view.first()

    def gatherCommands(self):
        keys=self.app.earman.keys()
        objects=self.app.earman.objects()
        state=('exec', 'any', 'any', 'any')
        exec_keys=self.app.earman.getStateKeys(
                state, keys)
        commands=exec_keys['']
        func_data={}
        for oname, fname in commands:
            objs=objects.get(oname, [])
            for obj in objs:
                func=getattr(obj, fname, None)
                if func:
                    signiture = inspect.signature(func)
                    data=self.getOptions(fname, signiture)
                    self.m_agents[fname]=func
                    func_data[fname]=data
        self.m_model.populateModel(func_data)
        self.setupView()
        self.updateModel()

    def getOptions(self, name, signiture):
        data=OrderedDict()
        filler=self.app.buffman.getFiller(name, {})
        prmts=signiture.parameters
        for (name, prmt) in prmts.items():
            if name in ['args', 'kwargs']:
                continue
            options= filler.get(name, [])
            if prmt.default!=inspect.Parameter.empty:
                options.insert(0, prmt.default)
            data[name]=options
        return data

    def connectEditline(self, kind='connect'):
        edit=self.app.plugman.getPlug('Editline')
        if edit and kind=='connect':
            edit.textChanged.connect(self.updateModel)
        elif edit and kind=='disconnect':
            edit.textChanged.disconnect(self.updateModel)

    def updateModel(self):
        edit=self.app.plugman.getPlug('Editline')
        text=edit.text()
        self.m_model.applyFilter(text)
        self.updateViewGeometry()

    def updateViewGeometry(self):
        hint=self.m_view.sizeHint()
        geometry=self.m_view.geometry()
        overlay=self.m_overlay.geometry()
        y=max(0, overlay.height()-hint.height())
        geometry.setX(0)
        geometry.setY(y)
        geometry.setSize(hint)
        self.m_view.setGeometry(geometry)

    def addAgent(self, name, data):
        self.m_agents[name]=data

    def getAgent(self, name):
        return self.m_agents.get(name, {})

    @tag([":(normal)", "<escape>/<c-[>(exec)"])
    def toggle(self):
        editline=self.app.plugman.getPlug('Editline')
        if editline and not self.activated:
            self.activate()
        elif editline and self.activated:
            self.octivate()

    def activate(self):
        editline=self.app.plugman.getPlug('Editline')
        if editline:
            super().activate()
            self.m_view.activate()
            self.connectEditline('connect')
            editline.activate(mode='exec',passive=['exec', 'any'])
            self.updateViewGeometry()

    def octivate(self):
        editline=self.app.plugman.getPlug('Editline')
        if editline:
            super().octivate()
            editline.octivate()
            self.connectEditline('disconnect')
            self.m_view.octivate()

    @tag('<c-l>/<tab>(exec)')
    def select(self):
        idx=self.m_view.currentIndex()
        item=self.m_model.itemFromIndex(idx)
        editline=self.app.plugman.getPlug('Editline')
        if item and editline:
            option=item.text()
            text=editline.edit.text()
            text=text.split(' ')[:-1]+[option]
            text=' '.join(text)
            editline.edit.setText(f'{text}')

    @tag('<c-j>(exec)')
    def down(self, xrange=[1]):
        self.m_view.goTo(kind='down', xrange=xrange)

    @tag('<c-k>(exec)')
    def up(self, xrange=[1]):
        self.m_view.goTo(kind='up', xrange=xrange)

    @tag('<c-m>/<return>(exec)')
    def act(self, command=None):
        if not command:
            edit=self.app.plugman.getPlug('Editline')
            command=edit.text().strip()
        self.toggle()
        if command:
            command = tuple(command.split(' '))
            func=self.m_agents.get(command[0], None)
            if func:
                try:
                    func(*command[1:])
                except:
                    if command[0]=='quit':
                        raise
