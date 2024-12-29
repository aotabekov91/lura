import math
import functools
import subprocess

from PyQt6 import QtCore, QtGui, QtWidgets

from plug import Plug

class BrowserLinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_hints={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('LinkHint')
        if holder:
            holder.addAgent('BrowserView', self)

    def activate(self, view=None, **kwargs):
        if view:
            selectors=self.getSelectors()
            code=view.assemble('webelem', 'find_css', selectors, False)
            callback=functools.partial(self.setLinks, view=view)
            view.runJSCode(code, resultCallback=callback)

    def octivate(self, view=None, **kwargs):
        for link in self.m_hints.values():
            label=link['label']
            label.hide()
            label.setParent(None)
        self.m_hints={}

    def goTo(self, link):
        print(link)

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

    def assignHints(self, links, model, view):
        hinter=self.app.plugman.getPlug('Hint')
        _, hints=hinter.generateHints(links)
        for hint, link in hints.items():
            link['hint']=hint
            label=QtWidgets.QLabel(hint)
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
        selectors=self.m_config.get(
                'Selectors', {})
        link_selectors=selectors.get('Links')
        return ','.join(link_selectors)

    def setLinks(self, elems, *, view):
        model=view.model()
        links=elems.get('result', [])
        self.assignHints(links, model, view)


    def checkHint(self, key, hint):
        if key:
            return key==hint[:len(key)]
        return False
