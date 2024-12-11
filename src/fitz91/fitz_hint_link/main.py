import math
import fitz
import subprocess

from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzLinkHint(Plug):

    def setup(self):
        super().setup()
        self.m_hint=''
        self.m_links={}
        self.m_hints={}
        self.m_length={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('LinkHint')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view=None, **kwargs):
        if view:
            self.cacheLinks(view)
            view.itemPainted.connect(self.paint)
            self.app.stateman.setFunctor(
                    functor=self.functor)
            view.redraw()

    def octivate(self, view=None, **kwargs):
        if view:
            self.m_hint=''
            view.itemPainted.disconnect(self.paint)
            view.redraw()
            self.app.stateman.setFunctor()

    def functor(self, key, earman):
        self.m_hint=key
        view=self.app.stateman.view()
        model=view.model()
        hints=self.hints(model)
        if self.m_hint in hints:
            link=hints.get(self.m_hint)
            self.goTo(link, model, view)
            link_hinter=self.app.plugman.getPlug(
                    'LinkHint')
            link_hinter.toggleHint()
            hinter=self.app.plugman.getPlug(
                    'Hint')
            hinter.toggleHint()
        for hint in hints:
            if self.checkHint(hint):
                view.redraw()
                return True
        self.m_hint=''
        view.redraw()
        return False

    def links(self, model):
        return self.m_links.get(model, None)

    def hints(self, model):
        return self.m_hints.get(model, {})

    def hintLength(self, model):
        return self.m_length.get(model, 0)

    def cacheLinks(self, view):
        model=view.model()
        links=self.links(model)
        if links is None:
            links=self.getLinks(model)
            self.m_links[model]=links
            self.assignHints(links, model)

    def cacheHints(self, hints, length, model):
        self.m_hints[model]=hints
        self.m_length[model]=length

    def assignHints(self, links, model):
        alist = []
        for element_links in links.values():
            alist+=element_links
        hinter=self.app.plugman.getPlug(
                'Hint')
        length, hints=hinter.generateHints(alist)
        self.cacheHints(hints, length, model)
        for hint, link in hints.items():
            link['hint']=hint

    def goTo(self, link, model, view):
        idx=link.get('index')
        element=model.element(idx)
        destination = link["link"].dest
        if destination.kind in [fitz.LINK_GOTO, fitz.LINK_GOTOR]:
            raise
        elif destination.kind in [fitz.LINK_URI]:
            cmd = ["qutebrowser", destination.uri]
            subprocess.Popen(cmd)
        elif destination.kind in [fitz.LINK_NAMED, fitz.LINK_LAUNCH]:
            data = model.modelData()
            uri = data.resolve_link(destination.uri)
            page, xpos, ypos = uri
            if math.isnan(xpos): 
                xpos=0.
            if math.isnan(ypos): 
                ypos=0.
            point = element.unify((xpos, ypos))
            view.goTo(page + 1, point.x(), point.y())

    def getLinks(self, model):
        links={}
        elements=model.elements()
        for element in elements.values():
            element_links=[]
            idx=element.index()
            links[idx]=element_links
            link = element.data().first_link
            while link:
                data = {}
                box=link.rect
                data["link"] = link
                width=box.x1-box.x0
                height=box.y1-box.y0
                rect=(box.x0, box.y0, width, height)
                data["box"] = element.unify(rect)
                data['index']=element.index()
                element_links += [data]
                link = link.next
        return links

    def paint(self, painter, ops, widget, item):
        painter.save()
        view=item.view()
        model=view.model()
        model_links=self.links(model)
        if model_links:
            element=item.element()
            idx=element.index()
            element_links=model_links.get(idx, [])
            if element_links:
                pen = QtGui.QPen(
                        QtCore.Qt.GlobalColor.red, 0.0)
                painter.setPen(pen)
                for link in element_links:
                    rect = []
                    hint=link.get("hint")
                    boxes = link.get("box")
                    if not self.checkHint(hint):
                        continue
                    if type(boxes) != list:
                        boxes = [boxes]
                    for box in boxes:
                        rect += [item.mapToItem(box, unified=True)]
                    painter.drawText(rect[0].topLeft(), hint)
        painter.restore()

    def checkHint(self, hint):
        if self.m_hint:
            key_length=len(self.m_hint)
            partial_hint=hint[:key_length]
            return partial_hint==self.m_hint
        return True
