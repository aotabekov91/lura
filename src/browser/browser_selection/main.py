import functools

from plug import Plug, deleg, tag

class BrowserSelection(Plug):

    views=['BrowserView']

    def setup(self):
        super().setup()
        self.m_selections={}
        self.app.buffman.viewCreated.connect(
                self.injectJSCode)

    def isCompatible(self, view):
        if view:
            for klass in view.__class__.__mro__:
                if klass.__name__ in self.views:
                    return True
        return False

    def injectJSCode(self, view):
        path=self.files.get('masha.js', None)
        if path and self.isCompatible(view):
            browser=view.browser()
            # func=functools.partial(self.start, view)
            # browser.loadFinished.connect(func)
            self.test(view, True)
            browser.selectionChanged.connect(self.updateSelection)

    def start(self, view, status):
        script=view.scriptize('selection', 'start')
        print(script)
        view.runJSCode(script)


    def test(self, view, status):
        if status:
            path=self.files.get('masha.js', None)
            view.injectJSCode(name='selection', path=path, subframes=True)

    def updateSelection(self):
        view=self.app.stateman.view()
        script=view.scriptize('selection', 'get_selection')
        print(script)
        callback=functools.partial(self._updateSelection, view)
        view.runJSCode(script, resultCallback=callback)

    def _updateSelection(self, view, box):
        self.m_selections[view]=[box]
        print(box)
        self.app.delegman.delegate(
                action='updateSelection',
                data={'view': view, 'box': [box]})

    @deleg('select@(any)[BrowserView]')
    def select(self, view=None, selection=None, **kwargs):
        if view and selection:
            sel_box=selection.get('box', None)
            cur_box=self.m_selections.get(view, None)
            if sel_box and sel_box!=cur_box:
                script=view.scriptize('selection', 'setSelection', sel_box[0])
                print(script)
                view.runJSCode(script) 

    @tag('!(normal)[BrowserView]')
    def Test(self):
        box=['0:10,0:12']
        view=self.app.stateman.view()
        selection=self.app.delegman.delegate(
                action='getSelection',
                data={'view': view})
        selection['box']=box
        self.select(view=view, selection=selection)
