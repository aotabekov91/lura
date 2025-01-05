import functools

from PyQt6 import QtWidgets, QtCore

from plug import Plug

class BrowserLinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_hints={}
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                'hint', 'link', 'BrowserView', 'start', self.start)
        self.app.delegman.addAgent(
                'hint', 'link', 'BrowserView', 'finish', self.finish)

    def start(self, view=None, **kwargs):
        if view:
            selectors=self.getSelectors()
            code=view.scriptize(
                    'elements', 'find_css', selectors, False)
            callback=functools.partial(self.setLinks, view=view)
            view.runJSCode(code, resultCallback=callback)

    def finish(self, view=None, **kwargs):
        for link in self.m_hints.values():
            label=link['label']
            label.hide()
            label.setParent(None)
        self.m_hints={}

    def goTo(self, link, *args):
        view=link['view']
        label=link['label']
        pos=label.geometry().center()
        pos= QtCore.QPointF(pos)
        view.fakeMouseEvent('move', position=pos)
        view.fakeMouseEvent(
                'press', position=pos, button='LeftButton')
        view.fakeMouseEvent(
                'release', position=pos, button='LeftButton')

    def functor(self, key, earman):
        partial=False
        for hint, link in self.m_hints.items():
            label=link['label']
            if self.checkHint(key, hint):
                if key==hint:
                    self.goTo(link)
                    hinter=self.app.plugman.getPlug('Hint')
                    hinter.octivate()
                    return True
                else:
                    label.show()
                    partial=True
            else:
                label.hide()
        return partial

    def assignHints(self, links, view):
        moder=self.app.stateman.moder()
        _, hints=moder.generateHints(links)
        for hint, link in hints.items():
            link['hint']=hint
            link['view']=view
            label=QtWidgets.QLabel(hint, objectName='HintLabel')
            label.setParent(view)
            rects=link.get('rects')
            link['label']=label
            if rects:
                rect=rects[0]
                top=int(rect['top'])
                left=int(rect['left'])
                width=int(rect['width'])
                height=int(rect['height'])
                label.setGeometry(left, top, width, height)
                label.show()
        self.m_hints=hints
        self.app.stateman.setFunctor(
                functor=self.functor)

    def getSelectors(self):
        selectors=self.m_config.get('Selectors', {})
        link_selectors=selectors.get('Links')
        return ','.join(link_selectors)

    def setLinks(self, elems, *, view):
        links=elems.get('result', [])
        self.assignHints(links, view)

    def checkHint(self, key, hint):
        return key and key==hint[:len(key)]
