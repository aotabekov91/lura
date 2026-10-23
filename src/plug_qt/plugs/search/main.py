from PyQt6 import QtCore

from plug import Plug, tag, deleg

class Search(Plug, QtCore.QObject):

    searchReady=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_data={}
        self.m_current={}
        self.searchReady.connect(self.jump)

    @deleg('setCurrentIndex@(search)')
    def setCurrentIndex(self, view=None, idx=None, **kwargs):
        self.m_current[view]=idx

    @deleg('currentIndex@(search)')
    def currentIndex(self, view=None, **kwargs):
        return self.m_current.get(view, None)

    def jump(self, data):
        view=data.get('view')
        found=data.get('results')
        subview=self.app.stateman.subview()
        if view==subview and found:
            self.app.stateman.activate(mode='search', submode='jump')
            self.next()
            raise

    @tag('{/}(normal)')
    def activate(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        editor=self.app.plugman.getPlug('Editline')
        agent=self.app.delegman.getAgent(
                mode='search', action='search', view=view)
        if agent and editor and view:
            editor.activate(
                    label='/', mode='search', passive=['search', 'any'])

    @tag('<c-m>/<return>/<enter>(search)')
    def search(self, view=None, search=None, **kwargs):
        view=view or self.app.stateman.subview()
        editor=self.app.plugman.getPlug('Editline')
        if editor and search is None:
            search=editor.text()
        agent=self.app.delegman.getAgent(
                mode='search',
                action='search',
                view=view)
        if agent:
            found=agent(view=view, search=search, **kwargs) 
            self.m_data[view]={'search': search, 'idx': 0, 'results': found}
            self.updateInfo(view=view)
            if found:
                view.activate(mode='search', submode='jump')
                self.next()

    @tag('{/}(search[jump])')
    def activateEdit(self):
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.activate(
                    label='/', keep=True, mode='search', passive=['search', 'any'])

    @tag('<c-[>/<escape>(search[any])')
    def octivate(self, view=None, **kwargs):
        powerline=self.app.plugman.getPlug('Powerline')
        if powerline:
            powerline.setInfo()
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.octivate()
        self.app.stateman.activate(mode='normal')

    def updateInfo(self, view=None, **kwargs):
        powerline=self.app.plugman.getPlug('Powerline')
        data=self.m_data.get(view, None)
        if data:
            idx=self.currentIndex(view=view)
            count=len(data['results'])
            if powerline:
                info=f'{idx}/{count}'
            else:
                info=None
            powerline.setInfo(info)

    @tag('n/j(search[jump])')
    def next(self, view=None, xrange=[1], **kwargs):
        view=view or self.app.stateman.subview()
        self.delegate(action='goTo', kind='next', xrange=xrange, **kwargs)

    @tag('p/k(search[jump])')
    def prev(self, view=None, xrange=[1], **kwargs):
        view=view or self.app.stateman.subview()
        self.delegate(action='goTo', kind='prev', xrange=xrange, **kwargs)

    @tag('gg(search[jump])')
    def first(self, **kwargs):
        self.delegate(action='goTo', kind='first', **kwargs)

    @tag('G(search[jump])')
    def last(self, **kwargs):
        self.delegate(action='goTo', kind='last', **kwargs)

    @tag('G(search[jump])')
    def goTo(self, xrange=None, **kwargs):
        self.delegate(action='goTo', xrange=xrange, kind=None, **kwargs)

    def delegate(self, view=None, action=None, **kwargs):
        view=view or self.app.stateman.subview()
        data=self.m_data.get(view, None)
        if data:
            kwargs['data']=data
            self.app.delegman.delegate(
                    action=action,
                    mode='search',
                    view=view,
                    data=kwargs)
        else:
            self.octivate()
        self.updateInfo(view=view)
