from PyQt6 import QtCore

from plug import Plug, tag

class Search(Plug, QtCore.QObject):

    searchReady=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_agents={}
        self.m_current=None
        self.searchReady.connect(self.jump)

    def jump(self, data):
        view=data.get('view')
        found=data.get('results')
        subview=self.app.stateman.subview()
        if view==subview and found:
            self.app.stateman.activate(mode='search', submode='jump')
            self.next()

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, view=None):
        if view:
            for klass in view.__class__.__mro__:
                name=klass.__name__
                agent=self.m_agents.get(name, None)
                if agent:
                    return agent

    @tag('{/}(normal)')
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(view=view)
        editor=self.app.plugman.getPlug('Editline')
        if agent and editor:
            editor.activate(
                    label='/', mode='search', passive=['search', 'any'])

    @tag('<c-m>/<return>/<enter>(search)')
    def search(self, view=None, search=None, **kwargs):
        if not view:
            view=self.app.stateman.subview()
        agent=self.getAgent(view=view)
        if search is None:
            editor=self.app.plugman.getPlug('Editline')
            search=editor.text()
        if agent:
            self.m_current=search
            agent.activate(action='search', view=view, search=search, **kwargs) 
            self.updateInfo()

    @tag('{/}(search[jump])')
    def activateEdit(self):
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.activate(
                    label='/', keep=True, mode='search', passive=['search', 'any'])

    @tag('<c-[>/<escape>(search[any])')
    def octivate(self, view=None, **kwargs):
        self.m_current=None
        if not view:
            view=self.app.stateman.subview()
        if view:
            self.search(view=view, search='')
        powerline=self.app.plugman.getPlug('Powerline')
        if powerline:
            powerline.setInfo()
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.octivate()
        self.app.stateman.activate(mode='normal')

    def updateInfo(self):
        view=self.app.stateman.subview()
        agent=self.getAgent(view=view)
        powerline=self.app.plugman.getPlug('Powerline')
        if agent and powerline:
            count=agent.count()
            if count:
                idx=agent.currentIndex()
                info=f'{idx}/{count}'
                powerline.setInfo(info)

    @tag('n/j(search[jump])')
    def next(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.subview()
        agent=self.getAgent(view=view)
        if agent and self.m_current :
            agent.activate(
                    action='goTo', 
                    kind='next', 
                    view=view, 
                    xrange=xrange,
                    search=self.m_current, 
                    **kwargs) 
            self.updateInfo()

    @tag('p/k(search[jump])')
    def previous(self, view=None, xrange=[1], **kwargs):
        if not view:
            view=self.app.stateman.subview()
        agent=self.getAgent(view=view)
        if agent and self.m_current :
            agent.activate(
                    action='goTo', 
                    kind='previous', 
                    view=view, 
                    xrange=xrange,
                    search=self.m_current, 
                    **kwargs) 
            self.updateInfo()
